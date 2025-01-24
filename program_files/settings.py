import os
import json
import tkinter as tk
from tkinter import filedialog
from config import SETTINGS_FILE

def load_settings():
    """Load settings from the settings file or set defaults."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    else:
        settings = {"download_path": SETTINGS_FILE, "file_type": ".docx"}
        save_settings(settings)
    return settings

def save_settings(settings):
    """Save settings to the settings file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=1)

def set_download_path(download_path_entry, settings):
    folderpath = filedialog.askdirectory(title="Select Download Path")
    if folderpath:
        download_path_entry.config(state="normal")
        download_path_entry.delete(0, tk.END)
        download_path_entry.insert(0, folderpath)
        download_path_entry.config(state="readonly")
        settings["download_path"] = folderpath
        save_settings(settings)