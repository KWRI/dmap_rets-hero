# RETS Hero (FreeSimpleGUI Client)

Interactive desktop helper to explore RETS metadata and run ad‑hoc DMQL searches using a lightweight GUI (`rets_hero.py`).

## 1. Features

* Login to a RETS endpoint
* List all resources (e.g. Property, Office, Agent)
* List classes for a selected resource
* Inspect table (field) metadata for a resource/class
* Execute DMQL searches with a configurable limit
* View results or metadata in a scrollable popup window

## 2. Requirements

* Python 3.8+ (earlier may work, not tested)
* Packages:
  * `rets` (Python RETS client library)
  * `FreeSimpleGUI` (drop‑in like PySimpleGUI; installable via pip)
  * (Standard library modules already included: `json`, `tkinter`, etc.)

Install dependencies:

```Shell
pip install rets FreeSimpleGUI
```

> If `FreeSimpleGUI` is not available in PyPI for your environment, substitute with `PySimpleGUI` and adjust the import in the script (`import PySimpleGUI as sg`).

## 3. File Overview

`rets_hero.py` – main executable script providing the GUI.

## 4. Running the App

From the `rets_hero` directory:

```Shell
python rets_hero.py
```

If on Linux and you want to run it directly:

```Shell
chmod +x rets_hero.py
./rets_hero.py
```

## 5. UI Workflow

1. Enter credentials:
   * Login URL
   * Username
   * Password (masked)
2. Click "Initialize Client" – a success popup should appear if authenticated.
3. Use the action buttons:
   * "All Resources": fetches and displays resource metadata.
   * "All Classes": requires a Resource (e.g. `Property`); lists classes (e.g. `Listing`).
   * "Metadata": requires Resource + Class; shows table/field metadata.
   * "Search": runs a DMQL query against the chosen resource/class.

## 6. Fields Explained

| Field         | Purpose                   | Example                               |
| ------------- | ------------------------- | ------------------------------------- |
| Login URL     | RETS login endpoint       | `https://rets.example.com/rets/login` |
| Resource Name | RETS resource container   | `Property`                            |
| Class Name    | Class within the resource | `Listing`                             |
| DMQL Query    | Filter expression         | `(ListPrice=150000+)`                 |
| Limit         | Max records to fetch      | `25`                                  |

## 7. DMQL Query Examples

Basic price minimum:

```
(ListPrice=300000+)
```

Price range:

```
(ListPrice=300000-500000)
```

Multiple conditions (AND):

```
((ListPrice=300000-500000),(BedsTotal=3+))
```

OR logic (depends on server dialect – often comma is AND and pipe may emulate OR if supported):

```
((City=Austin)|(City=Cedar Park))
```

Always consult the specific MLS RETS metadata for exact field names and allowed values.

## 8. Output

Results and metadata open in a separate modal window with a scrollable multiline text area. You can copy text directly. Close the window to return to the main interface.

## 9. Troubleshooting

| Issue                     | Possible Cause              | Fix                                                                                  |
| ------------------------- | --------------------------- | ------------------------------------------------------------------------------------ |
| Login fails               | Bad credentials / wrong URL | Verify credentials; confirm RETS URL ends with `login` path                          |
| Empty search results      | Query too restrictive       | Test a simpler query like `(ListPrice=0+)`                                           |
| Unicode / encoding errors | MLS sends unusual charset   | Ensure `rets` package up to date; try setting locale `export PYTHONIOENCODING=UTF-8` |
| GUI won't start (Linux)   | Missing Tk bindings         | Install system packages: `sudo apt-get install python3-tk`                           |

## 10. Security Notes

* Do NOT hardcode production credentials in the script.
* Avoid committing credentials to version control.
* Rotate RETS credentials periodically per MLS policy.

## 11. Customization Ideas

* Add export to CSV for search results.
* Add paging or offset controls.
* Cache metadata locally to reduce repeated calls.
* Add a status bar / progress indicator for large searches.

## 12. Minimal Code Snippet (Entry Point)

```Python
if __name__ == '__main__':
	 main()
```

## 13. Known Limitations

* Script uses a global `rets_client`; not ideal for multi-session use.
* No persistent configuration file; defaults are embedded.
* Error handling is broad (`except Exception`)—can be refined.

## 14. Contributing

1. Fork / branch
2. Make changes
3. Add concise comments for new UI elements
4. Submit PR with screenshots (optional)

## 15. License

Internal / TBD (add license section when determined).

***

Questions or improvements welcomed—extend the GUI to fit your MLS workflow.
