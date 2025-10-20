#!/usr/bin/env python3
"""RETS helper GUI with crash-safe single-window design.

Why this refactor:
  - Previous version spawned extra top-level windows; on some WSL / remote X setups
    (e.g. VS Code Interactive / Jupyter kernel) Tk window destruction during clipboard
    operations caused: X connection to :0 broken.
  - Now we use ONE main window with an output pane, eliminating additional Toplevels.
  - Added headless fallback for notebook / no DISPLAY environments.
  - Added robust copy / save actions without disabling the text widget.
"""

from __future__ import annotations

import os
import sys
import json
from typing import Any

# Prefer PySimpleGUI; fall back to FreeSimpleGUI if aliased that way
try:  # pragma: no cover - import guard
    import PySimpleGUI as sg  # type: ignore
except Exception:  # pragma: no cover
    import FreeSimpleGUI as sg  # type: ignore

from rets import Session  # type: ignore

# Add configurable RETS protocol/version & user agent (defaults, can be overridden by GUI)
DEFAULT_RETS_VERSION = os.environ.get("RETS_VERSION", "RETS/1.8")   # Try RETS/1.7.2 if RETS/1.8 fails
DEFAULT_RETS_USER_AGENT = os.environ.get("RETS_USER_AGENT", "rets-hero/0.1")


rets_client = None  # Global session


# ----------------------------- Environment Helpers ----------------------------- #
def running_in_notebook() -> bool:
    try:  # pragma: no cover - runtime detection
        from IPython import get_ipython  # type: ignore
        ip = get_ipython()
        return bool(ip and getattr(ip, 'config', None) and 'IPKernelApp' in ip.config)
    except Exception:
        return False


def gui_supported() -> bool:
    if sys.platform.startswith(('win', 'darwin')):
        return True
    return bool(os.environ.get('DISPLAY'))  # Linux/WSL


def safe_json(data: Any) -> str:
    try:
        if isinstance(data, (dict, list)):
            return json.dumps(data, indent=4, ensure_ascii=False)
        return json.dumps(data, indent=4, ensure_ascii=False) if not isinstance(data, str) else data
    except Exception:
        return str(data)


# ----------------------------- Download Directory (Manual) ----------------------------- #
# Removed auto-detection per user request. A text field in the GUI will collect the
# desired download directory. We keep simple helpers for extension & fallback only.


def ensure_extension(path: str, default_ext: str = '.txt') -> str:
    base, ext = os.path.splitext(path)
    if ext:
        return path
    return path + default_ext


def first_writable_path(preferred_dir: str, filename: str) -> str:
    candidates = [preferred_dir, os.path.expanduser('~'), '/tmp', os.getcwd()]
    for d in candidates:
        try:
            if os.path.isdir(d) and os.access(d, os.W_OK):
                return os.path.join(d, filename)
        except Exception:
            continue
    return os.path.join(os.getcwd(), filename)


# ----------------------------- Core RETS Ops ----------------------------- #
def initialize_rets_client(values) -> bool:
    global rets_client
    login_url = values.get('-LOGIN_URL-')
    username = values.get('-USERNAME-')
    password = values.get('-PASSWORD-')
    rets_version = values.get('-RETS_VERSION-') or DEFAULT_RETS_VERSION
    rets_user_agent = values.get('-RETS_UA-') or DEFAULT_RETS_USER_AGENT

    if not all([login_url, username, password, rets_version, rets_user_agent]):
        popup_warn("Please fill in all credential fields.")
        return False

    try:
        # Some rets libs accept version= and user_agent=; if not, we still set headers below.
        try:
            rets_client = Session(
                login_url,
                username,
                password,
                version=rets_version,              # may be ignored if lib doesn't support
                user_agent=rets_user_agent,        # optional
            )
        except TypeError:
            # Fallback if signature does not accept those kwargs
            rets_client = Session(login_url, username, password)

        # Force headers in case constructor didn't
        # (header must include exact string with RETS/ prefix)
        hdrs = getattr(rets_client, "http_headers", {})
        try:
            hdrs['RETS-Version'] = rets_version
            hdrs.setdefault('User-Agent', rets_user_agent)
            # Some servers also expect Accept + UA authorization style
            hdrs.setdefault('Accept', '*/*')
        except Exception:
            pass

        rets_client.login()
        popup_info(f"Logged in (RETS-Version={rets_version}; UA={rets_user_agent})")
        return True
    except Exception as e:  # pragma: no cover
        popup_error(f"Failed to initialize RETS client: {e}")
        rets_client = None
        return False


def fetch_resources():
    return rets_client.get_resource_metadata()


def fetch_classes(resource: str):
    return rets_client.get_class_metadata(resource)


def fetch_metadata(resource: str, klass: str):
    return rets_client.get_table_metadata(resource, klass)


def run_search(resource: str, klass: str, dmql: str, limit: int):
    return list(rets_client.search(resource=resource, resource_class=klass, dmql_query=dmql, limit=limit))


# ----------------------------- Popup Abstractions ----------------------------- #
def popup_info(msg: str):
    try:
        sg.popup(msg, title="Info", keep_on_top=True)
    except Exception:
        print(f"INFO: {msg}")


def popup_warn(msg: str):
    try:
        sg.popup(msg, title="Warning", keep_on_top=True)
    except Exception:
        print(f"WARNING: {msg}")


def popup_error(msg: str):
    try:
        sg.popup_error(msg, title="Error", keep_on_top=True)
    except Exception:
        print(f"ERROR: {msg}")


# ----------------------------- GUI Construction ----------------------------- #
def build_window():
    creds_col = [
        [sg.Text("Login URL:"), sg.Input("https://rets.example.com/login", key='-LOGIN_URL-', size=(55, 1))],
        [sg.Text("Username:"), sg.Input("", key='-USERNAME-', size=(55, 1))],
        [sg.Text("Password:"), sg.Input("", key='-PASSWORD-', password_char='*', size=(55, 1))],
        [sg.Text("RETS Version:"), sg.Input(DEFAULT_RETS_VERSION, key='-RETS_VERSION-', size=(20, 1)), sg.Text("User-Agent:"), sg.Input(DEFAULT_RETS_USER_AGENT, key='-RETS_UA-', size=(28, 1))],
        [sg.Text("Download Dir:"), sg.Input(os.getcwd(), key='-DL_DIR-', size=(45, 1)), sg.FolderBrowse("Browse")],
        [sg.Button("Initialize", key='-INIT-')],
    ]

    query_col = [
        [sg.Text("Resource:"), sg.Input("Property", key='-RESOURCE-', size=(20, 1)), sg.Text("Class:"), sg.Input("Listing", key='-CLASS-', size=(20, 1))],
        [sg.Text("DMQL:"), sg.Input("(ListPrice=150000+)", key='-DMQL-', size=(50, 1)), sg.Text("Limit:"), sg.Input("1", key='-LIMIT-', size=(6, 1))],
        [sg.Button("Resources", key='-GET_RES-'), sg.Button("Classes", key='-GET_CLASSES-'), sg.Button("Metadata", key='-GET_META-'), sg.Button("Search", key='-SEARCH-')],
    ]

    right_click = ['&Output', ['Copy All', 'Save As...']]

    output_frame = [
        [sg.Multiline('', key='-OUTPUT-', size=(110, 32), font=('Courier New', 10), right_click_menu=right_click, autoscroll=True, reroute_stdout=False, reroute_stderr=False, write_only=False, expand_x=True, expand_y=True)],
        [sg.Button('Copy All'), sg.Button('Save As...'), sg.Push(), sg.Button('Clear'), sg.Button('Exit')]
    ]

    layout = [
        [sg.Frame('Credentials', creds_col, expand_x=True)],
        [sg.Frame('Query', query_col, expand_x=True)],
        [sg.Frame('Output', output_frame, expand_x=True, expand_y=True)],
    ]

    return sg.Window("RETS Client", layout, resizable=True, finalize=True)


def write_output(window, title: str, data: Any):
    multiline = window['-OUTPUT-']
    content = safe_json(data)
    text = f"\n=== {title} ===\n{content}\n"
    multiline.print(text, end='')  # uses print-like semantics (safer for large text)
    # Ensure cursor view at end
    try:
        multiline.Widget.see('end')
    except Exception:
        pass


def handle_copy_all(window):
    try:
        data = window['-OUTPUT-'].get()
        sg.clipboard_set(data)
        popup_info("Copied output to clipboard.")
    except Exception as e:
        popup_error(f"Copy failed: {e}")


def handle_save(window):
    data = window['-OUTPUT-'].get()
    base_dir = window['-DL_DIR-'].get() or os.getcwd()
    base_dir = os.path.expanduser(base_dir)
    if not os.path.isdir(base_dir):
        try:
            os.makedirs(base_dir, exist_ok=True)
        except Exception as e:
            popup_error(f"Download directory invalid and could not be created: {e}")
            return

    path = sg.popup_get_file(
        "Save Output",
        save_as=True,
        default_extension=".txt",
        initial_folder=base_dir,
    )
    if not path:
        return
    path = ensure_extension(path, '.txt')
    try:
        if os.path.isdir(path):
            path = os.path.join(path, 'rets_output.txt')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)
        popup_info(f"Saved to {path}")
    except PermissionError:
        import datetime
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = f'rets_output_{ts}.txt'
        fallback_path = first_writable_path(base_dir, safe_name)
        try:
            with open(fallback_path, 'w', encoding='utf-8') as f:
                f.write(data)
            popup_warn(f"Permission denied writing original path. Saved instead to:\n{fallback_path}")
        except Exception as inner_e:
            popup_error(f"Save failed (permission + fallback error): {inner_e}")
    except IsADirectoryError:
        popup_error("Chosen path is a directory. Please select or enter a file name.")
    except OSError as e:
        popup_error(f"Save failed: {e}")


def gui_main():
    global rets_client
    window = build_window()

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == 'Clear':
            window['-OUTPUT-'].update('')
            continue

        if event in ('Copy All', 'Copy All:Output'):
            handle_copy_all(window)
            continue

        if event in ('Save As...', 'Save As...:Output'):
            handle_save(window)
            continue

        if event == '-INIT-':
            initialize_rets_client(values)
            continue

        # Require session for rest
        if not rets_client:
            popup_warn("Initialize first.")
            continue

        try:  # pragma: no cover - network dependent
            if event == '-GET_RES-':
                write_output(window, 'RESOURCES', fetch_resources())
            elif event == '-GET_CLASSES-':
                resource = values.get('-RESOURCE-')
                if not resource:
                    popup_warn('Provide resource')
                    continue
                write_output(window, f'CLASSES {resource}', fetch_classes(resource))
            elif event == '-GET_META-':
                resource = values.get('-RESOURCE-')
                klass = values.get('-CLASS-')
                if not resource or not klass:
                    popup_warn('Provide resource & class')
                    continue
                write_output(window, f'METADATA {resource}:{klass}', fetch_metadata(resource, klass))
            elif event == '-SEARCH-':
                resource = values.get('-RESOURCE-')
                klass = values.get('-CLASS-')
                dmql = values.get('-DMQL-')
                limit_raw = values.get('-LIMIT-', '1')
                if not all([resource, klass, dmql]):
                    popup_warn('Fill all search fields')
                    continue
                try:
                    limit = int(limit_raw or '1')
                except ValueError:
                    popup_warn('Limit must be integer')
                    continue
                results = run_search(resource, klass, dmql, limit)
                write_output(window, f'SEARCH {resource}:{klass}', results if results else 'No results')
        except Exception as e:
            popup_error(f"Operation failed: {e}")

    window.close()


# ----------------------------- Headless / Notebook Mode ----------------------------- #
def headless_notice():
    print("GUI not supported (running in notebook or missing DISPLAY). Running in headless mode.\n" \
          "You can still import this module and call functions programmatically.")


def main():  # entry point
    if running_in_notebook() or not gui_supported():
        headless_notice()
        return
    gui_main()


if __name__ == '__main__':
    main()