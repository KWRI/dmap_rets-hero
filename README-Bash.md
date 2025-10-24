# RETS Hero (Linux/macOS Bash Installation & Run Guide)

This guide converts the Windows/PowerShell instructions into portable **bash** commands for Linux (tested on Ubuntu/Debian) and macOS. It uses the high‑performance **`uv`** package manager (preferred over classic `pip`).

---

## 1. Overview

RETS Hero is a single‑window Python GUI for ad‑hoc RETS metadata exploration and DMQL querying. It uses:

* `rets` (Python RETS client library)
* `FreeSimpleGUI` (Tkinter-based GUI)

You will:

1. Install `uv`
2. Create a virtual environment
3. Add dependencies
4. (Optional) set environment variables
5. Run the app

---

## 2. Prerequisites


| Item        | Notes                                                                       |
| ------------- | ----------------------------------------------------------------------------- |
| Python 3.8+ | Recommended 3.12 if available. Must be on PATH (`python3 --version`).       |
| Tk / Tcl    | Usually bundled with system Python; if missing install via package manager. |
| Git         | Needed to clone the repo if not already present.                            |
| Internet    | Required to install dependencies and fetch RETS data.                       |

Check Python:

```bash
python3 --version
```

If Python is missing:

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-tk
```

Fedora:

```bash
sudo dnf install -y python3 python3-tkinter
```

macOS (if using Homebrew):

```bash
brew install python-tk
```

Confirm Tkinter works (optional quick test):

```bash
python3 - <<'PY'
import tkinter as tk; print('Tkinter OK, version:', tk.TkVersion)
PY
```

---

## 3. Install `uv`

Official install script:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

Add `uv` to PATH if not auto-configured (re-open shell or source profile). Common install path: `$HOME/.local/bin`.

Verify:

```bash
~/.local/bin/uv --version || uv --version
```

If not found, ensure this is in your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
source "$HOME/.bashrc"
```

---

## 4. Obtain Project

If you don't already have the folder:

```bash
cd "$HOME"  # or any workspace directory
# Replace <repo-url> with the correct Git URL
git clone <repo-url> dmap_rets-hero
cd dmap_rets-hero
```

If already present:

```bash
cd "$HOME/dmap_rets-hero"  # adjust path if different
```

---

## 5. Create Virtual Environment (uv)

```bash
uv venv .venv
```

You can optionally "activate" but `uv run` makes that unnecessary.

---

## 6. Install Dependencies

```bash
uv add rets FreeSimpleGUI
```

If a lock file (`uv.lock`) changed or you pulled updates:

```bash
uv sync
```

(Generates or updates `pyproject.toml` and `uv.lock` for reproducibility.)

---

## 7. Run the Application

```bash
uv run python rets-hero.py
```

If you get a display error: ensure you are not in a headless SSH session without X forwarding. For remote Linux you might need:

```bash
sudo apt install -y xauth
# Reconnect with: ssh -X user@host
```

macOS users should simply see the window appear.

---

## 8. Environment Variables (Optional)

If the app expects credentials or RETS settings via environment variables, you can export them before running:

```bash
export RETS_LOGIN_URL='https://example.com/login'
export RETS_USERNAME='myuser'
export RETS_PASSWORD='mypassword'
uv run python rets-hero.py
```

Persist them by adding the lines to `~/.bashrc` or using a `.env` loader (not included by default).

---

## 9. Typical Workflow

1. Provide Login URL, Username, Password.
2. Adjust RETS Version / User-Agent if required by provider.
3. Click Initialize.
4. Explore Resources / Classes / Metadata / Search.
5. Use Copy / Save / Clear for output management.
6. Exit via the window close button or provided Exit control.

---

## 10. Bash Helper Function (Optional Shortcut)

Add a function to launch RETS Hero quickly. Append to `~/.bashrc`:

echo "alias rets='cd /home/kwrllc/onedrive-kwrllc/git/dmap\_rets-hero && uv run python rets-hero.py'" >> \~/.bashrc
source \~/.bashrc

Reload:

```bash
echo "alias rets='cd /home/kwrllc/onedrive-kwrllc/git/dmap_rets-hero && uv run python rets-hero.py'" >> ~/.bashrc
source ~/.bashrc
```

Run:

```bash
rets
```

---

## 11. Updating / Pulling Changes

```bash
cd "$HOME/dmap_rets-hero"
git pull
uv sync  # Ensures env matches updated lock/deps
```

## 14. Quick Start (Condensed)

```Shell
# Install uv
curl -Ls https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Clone
cd "$HOME"
git clone <repo-url> dmap_rets-hero
cd dmap_rets-hero

# Env + deps
uv venv .venv
uv add rets FreeSimpleGUI

# Run
uv run python rets-hero.py
```

---

## 15. Notes

* Replace `<repo-url>` with the actual Git repository (HTTPS recommended).
* `rets` and `FreeSimpleGUI` must exist on PyPI; if internal forks are used, adjust to direct URLs or local paths.
* For reproducibility in CI, commit `uv.lock`.
