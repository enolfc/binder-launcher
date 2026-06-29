# Binder wrapper repo

Minimal Binder wrapper that accepts launch parameters, writes them to `/home/jovyan/work/.env`, pulls a target Git repository, overlays it into `/home/jovyan/work`, and redirects to the requested notebook.

## Binder URL shape

Use Binder's `urlpath` to call the wrapper extension:

```text
https://binder.ethz.ch/v2/gh/recap/binder-launcher/HEAD?urlpath=binder-launch%3Frepo%3Dhttps%3A%2F%2Fgithub.com%2Frecap%2FDataLens%26branch%3Dmain%26notebookpath%3DDataLens_EDA.ipynb%26csv_url%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2FAria-Dolatabadian%2FPearson-Correlation-Matrix%2Frefs%2Fheads%2Fmain%2Fcorr_data.csv
```

Decoded inner route:

```text
binder-launch?repo=https://github.com/ORG/TARGET_REPO&branch=main&notebookpath=notebook.ipynb&csv_url=https://example.org/data.csv&dataset_pid=doi:10.1234/abcd
```

The extension writes:

```text
/home/jovyan/workspace/.env
```

with:

```dotenv
CSV_URL='https://example.org/data.csv'
DATASET_PID='doi:10.1234/abcd'
```

## Notebook usage

```python
from dotenv import load_dotenv
import os

load_dotenv()

CSV_URL = os.getenv("CSV_URL")
```
