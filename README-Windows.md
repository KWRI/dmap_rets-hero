# RETS Hero (Windows Installation & Run Guide)

This guide walks through installing and running **RETS Hero** on a Windows PC using the high‑performance **`uv`** package manager (recommended over classic `pip`). It is Windows‑specific; for cross‑platform usage see the main `README.md`.

***

## 1. Overview

RETS Hero is a single‑window Python GUI for ad‑hoc RETS metadata exploration and DMQL querying. It uses:

* `rets` library for RETS connectivity
* `FreeSimpleGUI` for the GUI (no fallback)

You will:

1. Install `uv`
2. Create a virtual environment
3. Add dependencies
4. (Optionally) set environment variables
5. Run the app

***

## 2. Prerequisites

| Item            | Notes                                                                                |
| --------------- | ------------------------------------------------------------------------------------ |
| Python          | Windows Store or python.org install (3.8+; 3.12 tested). Ensure `python` is in PATH. |
| Tkinter         | Bundled with standard Windows Python. No extra install normally required.            |
| PowerShell      | Version 5+ or Windows Terminal recommended.                                          |
| Internet access | Required to install dependencies and fetch RETS data.                                |

Check Python:

```PowerShell
python --version
```

If Python not found, install from <https://www.python.org/downloads/> and re‑open PowerShell.

***

## 3. Install `uv`

`uv` is a fast dependency + virtual environment manager.

```PowerShell
iwr https://astral.sh/uv/install.ps1 -UseBasicParsing | iex
```

Verify:

```PowerShell
uv --version
```

If not found, ensure `%USERPROFILE%\.local\bin` is in your PATH or restart the shell.

***

## 4. Clone / Obtain Project

If you have not already:

```PowerShell
# Navigate to a workspace directory
tcd ~  # or cd C:\dev

# Clone (replace URL if using internal repo)
git clone <repo-url> dmap_rets-hero
cd dmap_rets-hero
```

If you already have the folder, just `cd` into it.

***

## 5. Create Virtual Environment (with uv)

```PowerShell
uv venv .venv
```

(Optional) Specify interpreter version:

```PowerShell
uv venv .venv --python 3.14
```

Activate (optional; `uv run` can work without activation):

```PowerShell
./.venv/Scripts/Activate.ps1
```

Your prompt should show `(venv)` or similar.

To deactivate later:

```PowerShell
deactivate
```

***

## 6. Install Dependencies

Add required packages via `uv`:

```PowerShell
uv add rets FreeSimpleGUI
```

Optional extras:

```PowerShell
uv add IPython  # Enhanced notebook detection (not required)
```

This creates/updates `pyproject.toml` (if used) and a `uv.lock` for reproducible builds.

Reconcile environment (if lock changed):

```PowerShell
uv sync
```

***

## 7. Run the Application

Using `uv` (activation optional):

```PowerShell
uv run python rets-hero.py
```

If you see a message about headless mode, you may be in an environment without a GUI (e.g. remote session). On a standard desktop, the window should appear.

***

## 9. Typical Workflow

1. Enter Login URL, Username, Password.
2. Optionally adjust RETS Version / User-Agent fields.
3. Click **Initialize** (expects a successful RETS login).
4. Use buttons: Resources / Classes / Metadata / Search.
5. Right‑click output or use buttons to Copy / Save / Clear.
6. Exit via **Exit** or closing the window.

***

## 10. Updating / Adding Packages

```PowerShell
uv add <package>
uv remove <package>
uv sync          # ensure lock & environment remain consistent
```

To upgrade (if version pins later added):

```PowerShell
uv add <package>@latest
```

***

## 11. Uninstall / Cleanup

Remove the virtual environment:

```PowerShell
Remove-Item -Recurse -Force .venv
```

Remove the project directory (if desired):

```PowerShell
cd ..
Remove-Item -Recurse -Force dmap_rets-hero
```

***

## 12. Troubleshooting (Windows)

| Symptom                      | Cause                                 | Fix                                                            |
| ---------------------------- | ------------------------------------- | -------------------------------------------------------------- |
| `uv` not found               | PATH not updated                      | Restart PowerShell; ensure `%USERPROFILE%\.local\bin` in PATH. |
| Python not in PATH           | Installer option unchecked            | Repair install or add Python path manually.                    |
| GUI does not open            | Running in non‑GUI session (e.g. SSH) | Run locally or ensure X forwarding not needed on Windows.      |
| `ImportError: FreeSimpleGUI` | Package missing                       | `uv add FreeSimpleGUI` or reactivate venv.                     |
| RETS login fails             | Bad credentials / URL                 | Verify login endpoint and credentials correctness.             |
| Empty search results         | Query too restrictive                 | Try a broader DMQL: `(ListPrice=0+)`.                          |
| Access denied saving file    | Folder lacks permissions              | Choose a writable directory (Desktop/Documents).               |
| SSL / TLS errors             | Outdated cert store                   | Update Windows or install latest Python.                       |

Logs / output are shown inline in the GUI’s multiline panel; copy them via **Copy All**.

***

## 13. Suggested Version Pinning (Optional)

Add pins for stability (example — adjust to actual tested versions):

```PowerShell
uv add FreeSimpleGUI==4.* rets==1.*
```

Later upgrade intentionally:

```PowerShell
uv add FreeSimpleGUI@latest
```

***

## 14. Headless / Notebook Considerations

If run inside Jupyter on Windows, the script may detect notebook mode and suppress GUI. You can still import and call functions programmatically:

```PowerShell
uv run python - <<'PY'
import rets_hero  # if packaged
# (In current structure, use: import rets_hero as rh if module name adjusted)
PY
```

***

## 15. Contributing (Windows Focus)

1. Fork or create a feature branch.
2. Ensure clean environment: `uv sync`.
3. Implement changes; keep UI responsive (avoid blocking calls).
4. Test: initialize + one metadata fetch + one search.
5. Run lint/type checks if added in future (none mandatory yet).
6. Submit PR with screenshots of the Windows UI.

***

## 16. Security Notes

* Do not hardcode credentials.
* Prefer environment variables or prompt entry.
* Treat downloaded listing data as sensitive (MLS terms of use apply).

***

## 17. License / Internal Use

If distributing externally, add proper license text here (MIT, Apache 2.0, etc.). For internal tooling, mark repository access restrictions accordingly.

***

## 18. Quick Reference Cheat Sheet

```PowerShell
# Install uv
iwr https://astral.sh/uv/install.ps1 -UseBasicParsing | iex

# Setup
uv venv .venv
./.venv/Scripts/Activate.ps1
uv add rets FreeSimpleGUI

# Optional extras
uv add IPython

# Run
uv run python rets-hero.py

# Env overrides
$env:RETS_VERSION='RETS/1.7.2'
$env:RETS_USER_AGENT='rets-hero-demo/1.0'
uv run python rets-hero.py
```

***

## 19. FAQ (Windows)

| Question                    | Answer                                                                             |
| --------------------------- | ---------------------------------------------------------------------------------- |
| Can I skip activation?      | Yes, `uv run` works without activation if `.venv` exists.                          |
| Where is the venv stored?   | In the `.venv` folder at project root.                                             |
| How do I update all deps?   | `uv sync --frozen` ensures you are locked; remove pins then `uv add <pkg>@latest`. |
| Does RETS Hero auto‑update? | No; pull latest source and re‑run `uv add` if deps change.                         |
| Can I package into an EXE?  | Use PyInstaller after confirming dependencies (`uv add pyinstaller`).              |

***

**Enjoy building with RETS Hero on Windows!**

***

## 20. PowerShell Alias Setup (Optional)

You can create a convenient alias (e.g. `rh`) that runs RETS Hero from anywhere.

### 20.2 Persistent (add to PowerShell profile)

Check your profile path:

```PowerShell
$PROFILE
```

If file missing, create it:

```PowerShell
New-Item -ItemType File -Path $PROFILE -Force | Out-Null
```

Edit:

```PowerShell
notepad $PROFILE
```

Add lines:

```PowerShell
function Start-RetsHero {
	$path = "C:\Users\KWR LLC\OneDrive - Keller Williams Realty Inc\git\dmap_rets-hero"
	if (-not (Test-Path $path)) { Write-Host "Path not found: $path" -ForegroundColor Red; return }
	if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { Write-Host "uv not installed" -ForegroundColor Yellow; return }
	Push-Location $path
	uv run python rets-hero.py
	Pop-Location
}
Set-Alias rets Start-RetsHero
```

Reload profile:

```PowerShell
. $PROFILE
```

Run:

```PowerShell
rets
```

