# RETS Hero (Windows Installation & Run Guide)

This guide walks through installing and running **RETS Hero** on a Windows PC using the high‑performance **`uv`** package manager (recommended over classic `pip`). It is Windows‑specific; for cross‑platform usage see the main `README.md`.

For installation using linux bash, please view this document: [README-Bash.md](https://github.com/KWRI/dmap_rets-hero/blob/main/README-Bash.md)

---

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

---

## 2. Prerequisites


| Item            | Notes                                                                               |
| ----------------- | ------------------------------------------------------------------------------------- |
| Python          | Windows Store or python.org install (3.8+; 3.12 tested). Ensure`python` is in PATH. |
| Tkinter         | Bundled with standard Windows Python. No extra install normally required.           |
| PowerShell      | Version 5+ or Windows Terminal recommended.                                         |
| Internet access | Required to install dependencies and fetch RETS data.                               |

Check Python:

```PowerShell
python --version  # If python doesn't work, try py --version or python3 --version
```

If Python not found, install from [https://www.python.org/downloads/](https://www.python.org/downloads/) and re‑open PowerShell.

---

## 3. Install `uv`

`uv` is a fast dependency + virtual environment manager.

```PowerShell
iwr https://astral.sh/uv/install.ps1 -UseBasicParsing | iex
```
Make sure to exit PowerShell, and open it again to apply the update.

Verify:

```PowerShell
uv --version
```

If not found, ensure `%USERPROFILE%\.local\bin` is in your PATH or restart the shell.

---

## 4. Clone / Obtain Project

If you have not already:

```PowerShell
# Navigate to a workspace directory
tcd ~  # or cd C:\dev

# Clone (replace URL if using internal repo)
git clone https://github.com/KWRI/dmap_rets-hero dmap_rets-hero
cd dmap_rets-hero
```

If you already have the folder, just `cd` into it.

---

## 5. Create Virtual Environment (with uv)

```PowerShell
uv venv .venv
```

---

## 6. Install Dependencies

Add required packages via `uv`:

```PowerShell
uv sync
```

This creates/updates `pyproject.toml` (if used) and a `uv.lock` for reproducible builds.

Reconcile environment (if lock changed):

```PowerShell
uv sync
```

---

## 7. Run the Application

Using `uv` (activation optional):

```PowerShell
uv run python rets-hero.py
```

If you see a message about headless mode, you may be in an environment without a GUI (e.g. remote session). On a standard desktop, the window should appear.

---

## 9. Typical Workflow

1. Enter Login URL, Username, Password.
2. Optionally adjust RETS Version / User-Agent fields.
3. Click **Initialize** (expects a successful RETS login).
4. Use buttons: Resources / Classes / Metadata / Search.
5. Right‑click output or use buttons to Copy / Save / Clear.
6. Exit via **Exit** or closing the window.

---

## 10.  PowerShell Alias Setup (Optional)

You can create a convenient alias (e.g. `rh`) that runs RETS Hero from anywhere.

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
	$path = "C:\Path\To\dmap_rets-hero"
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
