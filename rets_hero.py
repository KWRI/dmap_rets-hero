#!/usr/bin/env python3

from importlib import metadata
import resource
import rets
from rets import Session
import json
import tkinter as tk
from tkinter import messagebox

def initialize_rets_client():
    global rets_client
    login_url = login_url_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if not login_url or not username or not password:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    try:
        rets_client = Session(login_url, username, password)
        messagebox.showinfo("Success", "RETS client initialized successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to initialize RETS client: {e}")


# Function to display resources in a new window
def show_all_resources():
    try:
        initialize_rets_client()
        rets_client.login()
        all_resources = rets_client.get_resource_metadata()
        resources_window = tk.Toplevel(root)
        resources_window.title("Available Resources")
        resources_text = tk.Text(resources_window, wrap=tk.WORD, width=80, height=20)
        resources_text.pack(padx=10, pady=10)
        resources_text.insert(tk.END, json.dumps(all_resources, indent=4))
        resources_text.config(state=tk.DISABLED)  # Make the text read-only
        close_button = tk.Button(resources_window, text="Close", command=resources_window.destroy)
        close_button.pack(pady=5)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch resources: {e}")

# Function to initialize the RETS client

        
def show_all_classes():
    try:
        initialize_rets_client()
        rets_client.login()
        resources = resource_name_entry.get()
        all_classes = rets_client.get_class_metadata(resources)
        resources_window = tk.Toplevel(root)
        resources_window.title("Available Classes")
        resources_text = tk.Text(resources_window, wrap=tk.WORD, width=80, height=20)
        resources_text.pack(padx=10, pady=10)
        resources_text.insert(tk.END, json.dumps(all_classes, indent=4))
        resources_text.config(state=tk.DISABLED)  # Make the text read-only
        close_button = tk.Button(resources_window, text="Close", command=resources_window.destroy)
        close_button.pack(pady=5)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch resources: {e}")
        
        
def show_metadata():
    try:
        initialize_rets_client()
        rets_client.login()
        resources = resource_name_entry.get()
        classes = class_name_entry.get()
        metadata = rets_client.get_table_metadata(resources, classes)
        resources_window = tk.Toplevel(root)
        resources_window.title("Metadata")
         # Create a frame to hold the Text widget and Scrollbar
        frame = tk.Frame(resources_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add a vertical scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        resources_text = tk.Text(frame, wrap=tk.WORD, width=80, height=20, yscrollcommand=scrollbar.set)
        resources_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        resources_text.insert(tk.END, json.dumps(metadata, indent=4))
        resources_text.config(state=tk.DISABLED)  # Make the text read-only
        # Configure the scrollbar to work with the Text widget
        scrollbar.config(command=resources_text.yview)
        close_button = tk.Button(resources_window, text="Close", command=resources_window.destroy)
        close_button.pack(pady=5)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch resources: {e}")
        
def search_properties():
    try:
        initialize_rets_client()
        rets_client.login()
        resources = resource_name_entry.get()
        classes = class_name_entry.get()
        dmql_query = dmql_query_entry.get()
        limit = limit_entry.get()

        # Convert the generator to a list
        search_props = list(rets_client.search(resource=resources, resource_class=classes, limit=int(limit), dmql_query=dmql_query))

        resources_window = tk.Toplevel(root)
        resources_window.title("Property Search")
        
        resources_text = tk.Text(resources_window, wrap=tk.WORD, width=80, height=20)
        resources_text.pack(padx=10, pady=10)

        # Display the first result if available
        if search_props:
            resources_text.insert(tk.END, json.dumps(search_props[0], indent=4))
        else:
            resources_text.insert(tk.END, "No results found.")

        resources_text.config(state=tk.DISABLED)  # Make the text read-only
        close_button = tk.Button(resources_window, text="Close", command=resources_window.destroy)
        close_button.pack(pady=5)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch resources: {e}")
        

# Create the main application window
root = tk.Tk()
root.title("RETS Client")

# Create input fields for credentials
tk.Label(root, text="Login URL:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
login_url_entry = tk.Entry(root, width=50)
login_url_entry.grid(row=0, column=1, padx=10, pady=5)
login_url_entry.insert(0, "https://rets.nlar.mlxmatrix.com/Rets/login.ashx")

tk.Label(root, text="Username:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
username_entry = tk.Entry(root, width=50)
username_entry.grid(row=1, column=1, padx=10, pady=5)
username_entry.insert(0, "SMARTERAGENTMOBILE")

tk.Label(root, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
password_entry = tk.Entry(root, width=50, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=5)
password_entry.insert(0, "#SMA@22bile")


# Create buttons for initializing the client and showing resources
initialize_button = tk.Button(root, text="Initialize Client", command=initialize_rets_client)
initialize_button.grid(row=3, column=0, columnspan=2, pady=10)

all_resources_button = tk.Button(root, text="All Resources", command=show_all_resources)
all_resources_button.grid(row=4, column=0, columnspan=2, pady=10)

# Create input fields for resource and class
tk.Label(root, text="Resource Name:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
resource_name_entry = tk.Entry(root, width=50)
resource_name_entry.grid(row=5, column=1, padx=10, pady=5)
resource_name_entry.insert(0, "Property")


all_classes_button = tk.Button(root, text="All Classes", command=show_all_classes)
all_classes_button.grid(row=6, column=0, columnspan=2, pady=10)


tk.Label(root, text="Class Name:").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
class_name_entry = tk.Entry(root, width=50)
class_name_entry.grid(row=7, column=1, padx=10, pady=5)
class_name_entry.insert(0, "Listing")

# Listing Metadata button
all_resources_button = tk.Button(root, text="Metadata", command=show_metadata)
all_resources_button.grid(row=8, column=0, columnspan=2, pady=10)



tk.Label(root, text="DMQL_Query:").grid(row=9, column=0, padx=10, pady=5, sticky=tk.W)
dmql_query_entry = tk.Entry(root, width=50)
dmql_query_entry.grid(row=9, column=1, padx=10, pady=5)
dmql_query_entry.insert(0, "(ListPrice=150000+)")

tk.Label(root, text="Limit:").grid(row=10, column=0, padx=10, pady=5, sticky=tk.W)
limit_entry = tk.Entry(root, width=50)
limit_entry.grid(row=10, column=1, padx=10, pady=5)
limit_entry.insert(0, "1")

# Create search button
search_button = tk.Button(root, text="Search", command=search_properties)
search_button.grid(row=11, column=0, columnspan=2, pady=10)















# Start the Tkinter event loop
root.mainloop()