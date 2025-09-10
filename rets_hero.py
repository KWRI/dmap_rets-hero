#!/usr/bin/env python3

import FreeSimpleGUI as sg
from rets import Session
import json
from importlib import metadata
import resource
import rets
from rets import Session
import json
import tkinter as tk
from tkinter import messagebox

# Global RETS client
rets_client = None

def initialize_rets_client(values):
    """Initializes the RETS client using credentials from the GUI."""
    global rets_client
    login_url = values['-LOGIN_URL-']
    username = values['-USERNAME-']
    password = values['-PASSWORD-']
    
    if not all([login_url, username, password]):
        sg.popup_warning("Please fill in all credential fields.")
        return False
        
    try:
        rets_client = Session(login_url, username, password)
        rets_client.login()
        sg.popup("Success", "RETS client initialized and logged in successfully!")
        return True
    except Exception as e:
        sg.popup_error(f"Failed to initialize RETS client: {e}")
        rets_client = None
        return False

def show_in_new_window(title, content):
    """Helper function to display content in a new window."""
    layout = [
        [sg.Multiline(content, size=(80, 20), disabled=True, key='-CONTENT-')],
        [sg.Button('Close')]
    ]
    window = sg.Window(title, layout, modal=True)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Close'):
            break
    window.close()

def main():
    global rets_client

    layout = [
        [sg.Text("Login URL:"), sg.Input(default_text="RETS URL", key='-LOGIN_URL-', size=(50, 1))],
        [sg.Text("Username:"), sg.Input(default_text="Username", key='-USERNAME-', size=(50, 1))],
        [sg.Text("Password:"), sg.Input(default_text="Password", key='-PASSWORD-', password_char='*', size=(50, 1))],
        [sg.Button("Initialize Client")],
        [sg.HSeparator()],
        [sg.Text("Resource Name:"), sg.Input(default_text="Property", key='-RESOURCE-', size=(50, 1))],
        [sg.Text("Class Name:"), sg.Input(default_text="Listing", key='-CLASS-', size=(50, 1))],
        [sg.Text("DMQL Query:"), sg.Input(default_text="(ListPrice=150000+)", key='-DMQL_QUERY-', size=(50, 1))],
        [sg.Text("Limit:"), sg.Input(default_text="1", key='-LIMIT-', size=(10, 1))],
        [sg.Button("All Resources"), sg.Button("All Classes"), sg.Button("Metadata"), sg.Button("Search")]
    ]

    window = sg.Window("RETS Client", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        
        if event == "Initialize Client":
            initialize_rets_client(values)
            continue

        # All subsequent actions require an initialized client
        if not rets_client:
            sg.popup_warning("Please initialize the RETS client first.")
            continue
            
        try:
            if event == "All Resources":
                all_resources = rets_client.get_resource_metadata()
                show_in_new_window("Available Resources", json.dumps(all_resources, indent=4))

            elif event == "All Classes":
                resource = values['-RESOURCE-']
                if not resource:
                    sg.popup_warning("Please enter a Resource Name.")
                    continue
                all_classes = rets_client.get_class_metadata(resource)
                show_in_new_window("Available Classes", json.dumps(all_classes, indent=4))

            elif event == "Metadata":
                resource = values['-RESOURCE-']
                r_class = values['-CLASS-']
                if not all([resource, r_class]):
                    sg.popup_warning("Please enter a Resource Name and Class Name.")
                    continue
                metadata = rets_client.get_table_metadata(resource, r_class)
                show_in_new_window("Metadata", json.dumps(metadata, indent=4))

            elif event == "Search":
                resource = values['-RESOURCE-']
                r_class = values['-CLASS-']
                dmql_query = values['-DMQL_QUERY-']
                limit = values['-LIMIT-']
                if not all([resource, r_class, dmql_query, limit]):
                    sg.popup_warning("Please fill in all fields for search.")
                    continue
                
                search_props = list(rets_client.search(resource=resource, resource_class=r_class, limit=int(limit), dmql_query=dmql_query))
                
                if search_props:
                    content = json.dumps(search_props, indent=4)
                else:
                    content = "No results found."
                show_in_new_window("Property Search Results", content)

        except Exception as e:
            sg.popup_error(f"An error occurred: {e}")

    window.close()

if __name__ == '__main__':
    main()
