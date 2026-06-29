from pathlib import Path

c.ServerApp.root_dir = str(Path.home() / "work")
c.ServerApp.log_level = "DEBUG"
c.ContentsManager.allow_hidden = True
