import os
import shlex
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote

import tornado.web
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.utils import url_path_join

HOME = Path.home()
WORK = HOME / "work"
TARGET = WORK / "target"
ENV_FILE = WORK / ".env"
KEEP = {".env", ".ipynb_checkpoints"}

RESERVED_PARAMS = {"repo", "branch", "urlpath", "subpath", "targetpath", "overwrite"}


def shell_escape_env_value(value: str) -> str:
    return shlex.quote(value)


def safe_remove_work_contents():
    WORK.mkdir(exist_ok=True)
    for item in WORK.iterdir():
        if item.name in KEEP:
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def write_env(params: dict[str, str]):
    lines = []
    for key, value in sorted(params.items()):
        env_key = "BINDER_PARAM_" + key.upper().replace("-", "_")
        if not env_key.replace("_", "").isalnum():
            continue
        lines.append(f"{env_key}={shell_escape_env_value(value)}")
    ENV_FILE.write_text("\n".join(lines) + "\n")


def git_clone(repo: str, branch: str | None):
    if TARGET.exists():
        shutil.rmtree(TARGET)

    cmd = ["git", "clone", "--depth", "1"]
    if branch:
        cmd += ["--branch", branch]
    cmd += [repo, str(TARGET)]

    subprocess.run(cmd, check=True, text=True, capture_output=True)


def copy_target_into_work():
    for item in TARGET.iterdir():
        if item.name == ".git":
            continue
        dest = WORK / item.name
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()
        shutil.move(str(item), str(dest))
    shutil.rmtree(TARGET)


class LaunchHandler(JupyterHandler):
    @tornado.web.authenticated
    def get(self):
        repo = self.get_argument("repo")
        branch = self.get_argument("branch", None)
        urlpath = self.get_argument("urlpath", "lab")
        overwrite = self.get_argument("overwrite", "1") == "1"

        params = {}
        for key, values in self.request.query_arguments.items():
            if key in RESERVED_PARAMS:
                continue
            # Tornado returns bytes; use last value for simplicity.
            params[key] = values[-1].decode("utf-8")

        try:
            if overwrite:
                safe_remove_work_contents()

            write_env(params)
            git_clone(repo, branch)
            copy_target_into_work()

        except subprocess.CalledProcessError as exc:
            self.set_status(500)
            self.write({
                "status": "error",
                "message": "git clone failed",
                "stdout": exc.stdout,
                "stderr": exc.stderr,
            })
            return
        except Exception as exc:
            self.set_status(500)
            self.write({"status": "error", "message": str(exc)})
            return

        self.redirect(url_path_join(self.base_url, urlpath))
