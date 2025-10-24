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
