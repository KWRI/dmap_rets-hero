# RETS Hero

Single–window Python GUI for exploring RETS metadata and issuing ad‑hoc DMQL searches (`rets-hero.py`).

***

## 1. What’s New (Current Script)

The refactored `rets-hero.py` now provides:

* One resilient main window (no extra `Toplevel` popups that can crash under remote X / WSL).
* Scrollable output pane with right‑click (Copy / Save) and dedicated buttons.
* Configurable RETS Version & User‑Agent (fields in GUI; environment variable overrides).
* Download directory selector for saving output.
* Headless fallback: skips GUI when run inside a Jupyter notebook or when no DISPLAY (Linux/WSL servers).
* Safer large text rendering (print semantics) and robust copy/save with permission fallbacks.

***

## 2. Prerequisites

* Python 3.8+ (3.12 works; earlier versions untested).
* Tkinter (bundled with standard Windows & macOS Python; on Debian/Ubuntu: `sudo apt-get install python3-tk`).
* RETS client library: `rets`.
* GUI library: Prefer `PySimpleGUI`; fallback to `FreeSimpleGUI` if needed.

Recommended: use a virtual environment located in the project root (`dmap_rets-hero/venv_rets-hero`).

***

## 3. Create & Activate Virtual Environment

Run these from the project directory (`dmap_rets-hero`).

### Windows (PowerShell)

```PowerShell
# Navigate to project root (adjust path as needed)
cd "PATH/TO/dmap_rets-hero"

# Create venv named venv_rets-hero
python -m venv venv_rets-hero

# (Optional) Allow script execution for this session if activation is blocked
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Activate (forward slashes work in PowerShell)
. "./venv_rets-hero/Scripts/Activate.ps1"

# Your prompt should show (venv_rets-hero)
```

Deactivate later with:

```PowerShell
deactivate
```

### Bash / Linux / macOS

```Shell
cd /path/to/dmap_rets-hero
python3 -m venv venv_rets-hero
source venv_rets-hero/bin/activate
# Prompt shows (venv_rets-hero)
```

Deactivate later with:

```Shell
deactivate
```

***

## 4. Install Dependencies

Use `requirements.txt` if present:

```Shell
pip install -r requirements.txt
```

If you prefer manual installs or need the fallback:

```Shell
pip install rets PySimpleGUI
# Fallback if PySimpleGUI fails or not desired
pip install FreeSimpleGUI
```

The script first tries `import PySimpleGUI as sg`; if that fails it attempts `import FreeSimpleGUI as sg`.

***

## 5. Environment Variable Overrides (Optional)

You can set these before running to override GUI defaults:

| Variable          | Purpose                     | Default         |
| ----------------- | --------------------------- | --------------- |
| `RETS_VERSION`    | Header `RETS-Version` value | `RETS/1.8`      |
| `RETS_USER_AGENT` | HTTP `User-Agent` header    | `rets-hero/0.1` |

Example (PowerShell):

```PowerShell
$env:RETS_VERSION = 'RETS/1.7.2'
$env:RETS_USER_AGENT = 'rets-hero-demo/1.0'
python rets-hero.py
```

Example (Bash):

```Shell
RETS_VERSION='RETS/1.7.2' RETS_USER_AGENT='rets-hero-demo/1.0' python3 rets-hero.py
```

***

## 6. Run the Application

From the activated virtual environment in project root:

```Shell
python rets-hero.py
```

Make script directly executable (Linux/macOS):

```Shell
chmod +x rets-hero.py
./rets-hero.py
```

Headless mode message appears if GUI cannot start (e.g., notebook environment or no DISPLAY). In that case you can import and call functions programmatically.

***

## 7. GUI Workflow

1. Fill credentials:
   * Login URL (e.g. `https://rets.example.com/login`)
   * Username
   * Password
   * (Optionally adjust RETS Version / User-Agent)
   * Download Dir (where saved output files go)
2. Click **Initialize**. A success popup confirms login; otherwise an error/warning.
3. Specify search context:
   * Resource (e.g. `Property`)
   * Class (e.g. `Listing`)
   * DMQL query (e.g. `(ListPrice=150000+)`)
   * Limit (integer)
4. Use action buttons:
   * **Resources** – lists all resource metadata.
   * **Classes** – lists classes for the given Resource.
   * **Metadata** – table/field metadata for Resource + Class.
   * **Search** – executes DMQL search; results shown in output pane.
5. Manage output:
   * Right‑click pane or use buttons: **Copy All**, **Save As...**, **Clear**.
   * Saved files default to `.txt`; fallback logic chooses a writable path if permissions block your target.
6. Exit with **Exit** or window close.

***

## 8. Primary Fields

| Field        | Description           | Example                          |
| ------------ | --------------------- | -------------------------------- |
| Login URL    | RETS login endpoint   | `https://rets.example.com/login` |
| Resource     | RETS resource name    | `Property`                       |
| Class        | Class within resource | `Listing`                        |
| DMQL         | Query expression      | `(ListPrice=150000+)`            |
| Limit        | Max records           | `25`                             |
| RETS Version | Protocol header       | `RETS/1.8`                       |
| User-Agent   | HTTP UA               | `rets-hero/0.1`                  |
| Download Dir | Save location         | `C:\Users\me\Desktop`            |

***

## 9. DMQL Examples

Minimum price:

```
(ListPrice=300000+)
```

Price range:

```
(ListPrice=300000-500000)
```

Multiple AND conditions:

```
((ListPrice=300000-500000),(BedsTotal=3+))
```

Possible OR (server dependent):

```
((City=Austin)|(City=Cedar Park))
```

Always verify field names against retrieved metadata.

***

## 10. Troubleshooting

| Issue                 | Cause                  | Resolution                                                   |
| --------------------- | ---------------------- | ------------------------------------------------------------ |
| Login fails           | Bad credentials / URL  | Confirm endpoint includes `login`; verify username/password. |
| Empty results         | Query too restrictive  | Try a very permissive query `(ListPrice=0+)`.                |
| Encoding errors       | MLS charset odd        | Upgrade `rets`; ensure UTF‑8 locale.                         |
| GUI fails on Linux    | Missing Tk             | `sudo apt-get install python3-tk`.                           |
| Save permission error | Directory not writable | Choose another folder; fallback auto-saves in home/temp.     |

***

## 11. Security Notes

* Avoid storing credentials in source or committing them.
* Rotate passwords per MLS policy.
* Treat output files containing listing data as sensitive.

***

## 12. Extensibility Ideas

* Export search results to CSV.
* Query paging / offsets.
* Local metadata caching.
* Progress indicator for long searches.
* Config file (`.retshero.toml`) for defaults.

***

## 13. Limitations

* Global `rets_client` (no multi-session isolation).
* Broad exception handling around network calls.
* No built‑in CSV export yet.

***

## 14. Contributing

1. Fork / branch.
2. Create / activate venv; install deps.
3. Make change; add comments near new UI elements.
4. Test login + sample query.
5. Submit PR (screenshots welcome).

***

