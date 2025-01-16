import os
import tkinter as tk
from document_handler import (
    upload_example_docs,
    upload_information_docs,
    save_docs,
    show_uploaded_files,
    clear_examples,
    clear_information,
    load_docs,
    generate_document
)
from settings import load_settings, save_settings, set_download_path

# File Paths
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "program_data")
SETTINGS_FILE = os.path.join(DATA_FILE_PATH, "settings.json")
DEFAULT_DOWNLOAD_DIR = os.path.join(DATA_FILE_PATH, "generated_docs")
    
if not os.path.exists(DEFAULT_DOWNLOAD_DIR):
    os.makedirs(DEFAULT_DOWNLOAD_DIR)
load_docs()
settings = load_settings(DEFAULT_DOWNLOAD_DIR)
default_download_path = settings.get("download_path", DEFAULT_DOWNLOAD_DIR)

# Create the main window
root = tk.Tk()
root.title("Document Generator")
root.geometry("600x700")

# Formatting Section
tk.Label(root, text="Describe The formatting of the document and upload examples of the format:").pack(anchor="center", padx=10, pady=5)
formatting_textbox = tk.Text(root, height=5, width=70)
formatting_textbox.pack(padx=10, pady=5)
tk.Button(root, text="Upload Example Documents", command=upload_example_docs).pack(pady=5)

# Information Section
tk.Label(root, text="Paste and upload any information needed for the document here:").pack(anchor="center", padx=10, pady=5)
information_textbox = tk.Text(root, height=5, width=70)
information_textbox.pack(padx=10, pady=5)
tk.Button(root, text="Upload Informational Documents", command=upload_information_docs).pack(pady=5)

# Download Path Section
tk.Label(root, text="Set File Download Location:").pack(anchor="center", padx=10, pady=5)
download_path_entry = tk.Entry(root, width=50)
download_path_entry.pack(pady=5)
download_path_entry.insert(0, default_download_path)
download_path_entry.bind("<Button-1>", lambda e: set_download_path(download_path_entry=download_path_entry, settings=settings))
download_path_entry.config(state="readonly")

# Filename Section
tk.Label(root, text="Set New File Name:").pack(anchor="center", padx=10, pady=5)
filename_entry = tk.Entry(root, width=50)
filename_entry.pack(pady=5)

# File Type Section
tk.Label(root, text="Select File Type:").pack(anchor="center", padx=10, pady=5)
file_type_options = [".docx", ".pdf", ".txt"]
file_type = tk.StringVar(value=settings["file_type"])

def update_file_type(*args):
    settings["file_type"] = file_type.get()
    save_settings(settings)

file_type.trace("w", update_file_type)
file_type_dropdown = tk.OptionMenu(root, file_type, *file_type_options)
file_type_dropdown.pack(pady=5)

# Generate Button
tk.Button(root, text="Generate", command=lambda: 
    generate_document(formatting_textbox=formatting_textbox, information_textbox=information_textbox, 
    download_path_entry=download_path_entry, filename_entry=filename_entry, file_type=file_type)).pack(pady=20)

# Show Uploaded Files Button
tk.Button(root, text="Show Uploaded Documents", command=lambda: show_uploaded_files(root=root)).pack(pady=5)

root.mainloop()