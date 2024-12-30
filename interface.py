import tkinter as tk
from tkinter import filedialog, messagebox
from docx import Document
import json
import os
from PyPDF2 import PdfReader

# Constants
EXAMPLE_DOCS_FILE = os.path.join(os.path.dirname(__file__), "example_docs.json")
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")
DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "generated_docs")

# Global variable dictionaries to store uploaded document text
example_doc_text = {}
information_doc_text = {}

def ensure_default_folder_exists():
    """Ensure the default folder for generated docs exists."""
    if not os.path.exists(DEFAULT_DOWNLOAD_DIR):
        os.makedirs(DEFAULT_DOWNLOAD_DIR)

def load_settings():
    """Load settings from the settings file or set defaults."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    else:
        settings = {"download_path": DEFAULT_DOWNLOAD_DIR}
        save_settings(settings)
    return settings

def save_settings(settings):
    """Save settings to the settings file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def save_example_docs():
    """Save example documents to file."""
    global example_doc_text
    with open(EXAMPLE_DOCS_FILE, "w") as f:
        json.dump(example_doc_text, f)

def load_example_docs():
    """Load example documents from file."""
    if os.path.exists(EXAMPLE_DOCS_FILE):
        global example_doc_text
        with open(EXAMPLE_DOCS_FILE, "r") as f:
            example_doc_text = json.load(f)

def delete_example_docs():
    """Delete example documents from file."""
    global example_doc_text

def clear_examples():
    """Clear uploaded document data and JSON files."""
    global example_doc_text
    response = messagebox.askyesno("Wipe Data", "Are you sure you want to remove all documents?")
    if response:
        example_doc_text = {}
        if os.path.exists(EXAMPLE_DOCS_FILE):
            save_example_docs()
    messagebox.showinfo("Success", "All example documents have been removed.")

def clear_information():
    """Clear uploaded information documents."""
    global information_doc_text
    response = messagebox.askyesno("Wipe Data", "Are you sure you want to remove all documents?")
    if response:
        information_doc_text = {}
    messagebox.showinfo("Success", "All information documents have been removed.")

def extract_text_from_document(filepath):
    """Extract text from the document."""
    if filepath.endswith(".docx"):
        doc = Document(filepath)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text
    elif filepath.endswith(".pdf"):
        try:
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text from PDF: {e}")
            return ""
    else:
        return ""
    
def upload_documents(doc_dict, type):
    """Upload and store documents in the given dictionary."""
    filepaths = filedialog.askopenfilenames(
        title=f"Upload {type} Documents",
        filetypes=[("Word and PDF Documents", "*.docx *.pdf")],
    )

    for filepath in filepaths:
        filename = os.path.basename(filepath)
        if filename in doc_dict:
            response = messagebox.askyesno("File Exists", f"{filename} already exists. Replace it?")
            if not response:
                continue

        # Extract and store document text
        doc_dict[filename] = extract_text_from_document(filepath)
        print(f"Document uploaded: {filename}")

def upload_example_docs():
    """Upload example documents."""
    global example_doc_text
    upload_documents(example_doc_text, "Example")
    save_example_docs()

def upload_information_docs():
    """Upload informational documents."""
    global information_doc_text
    upload_documents(information_doc_text, "Informational")

def set_download_path(event):
    folderpath = filedialog.askdirectory(title="Select Download Path")
    if folderpath:
        download_path_entry.config(state="normal")
        download_path_entry.delete(0, tk.END)
        download_path_entry.insert(0, folderpath)
        download_path_entry.config(state="readonly")
        settings["download_path"] = folderpath
        save_settings(settings)

def get_data_from_ai(formatting, information):
    """Placeholder for AI logic.""" 
    final_document_text = f"Formatting:\n{formatting}\n\n"
    final_document_text += f"Information:\n{information}\n\n"

    # Save the merged text to a Word document
    output_doc = Document()
    output_doc.add_heading("Sample Ai Document", level=1)
    output_doc.add_paragraph(final_document_text)
    return output_doc

def generate_document():
    """Generate the final document."""
    global example_doc_text, information_doc_text
    formatting = formatting_textbox.get("1.0", tk.END).strip()
    information = information_textbox.get("1.0", tk.END).strip()
    download_path = download_path_entry.get().strip()
    filename = filename_entry.get()

    # Append text from uploaded documents
    for name, text in example_doc_text.items():
        formatting += f"\n\nText from {name}:\n\n{text}"

    for name, text in information_doc_text.items():
        information += f"\n\nText from {name}:\n\n{text}"

    if not formatting or not information or not download_path or not filename:
        messagebox.showerror("Error", "Please fill in all fields and set a download path and file name.")
        return
    
    # Get the final document from the AI model
    output_doc = get_data_from_ai(formatting, information)
    output_filepath = f"{download_path}/{filename}.docx"
    output_doc.save(output_filepath)

    messagebox.showinfo("Success", f"Document generated and saved to {output_filepath}")
    print("Document generation completed.")

# Create the main window
root = tk.Tk()
root.title("Document Generator")
root.geometry("600x600")

# Load stuff
load_example_docs()
ensure_default_folder_exists()
settings = load_settings()
default_download_path = settings.get("download_path", DEFAULT_DOWNLOAD_DIR)

# Formatting Section
tk.Label(root, text="Describe the formatting of the document here:").pack(anchor="center", padx=10, pady=5)
formatting_textbox = tk.Text(root, height=5, width=70)
formatting_textbox.pack(padx=10, pady=5)

frame_example = tk.Frame(root)
frame_example.pack(pady=5)
tk.Button(frame_example, text="Upload Example Documents", command=upload_example_docs).pack(side=tk.LEFT, padx=5)
tk.Button(frame_example, text="Clear Example Documents", command=clear_examples).pack(side=tk.LEFT, padx=5)

# Information Section
tk.Label(root, text="Paste any information needed for the document here:").pack(anchor="center", padx=10, pady=5)
information_textbox = tk.Text(root, height=5, width=70)
information_textbox.pack(padx=10, pady=5)

frame_info = tk.Frame(root)
frame_info.pack(pady=5)
tk.Button(frame_info, text="Upload Information Documents", command=upload_information_docs).pack(side=tk.LEFT, padx=5)
tk.Button(frame_info, text="Clear Information Documents", command=clear_information).pack(side=tk.LEFT, padx=5)

# Download Path Section
tk.Label(root, text="Set File Download Location:").pack(anchor="center", padx=10, pady=5)
download_path_entry = tk.Entry(root, width=50)
download_path_entry.pack(pady=5)
download_path_entry.insert(0, default_download_path)
download_path_entry.config(state="readonly")
download_path_entry.bind("<Button-1>", set_download_path)

# Filename Section
tk.Label(root, text="Set Filename:").pack(anchor="center", padx=10, pady=5)
filename_entry = tk.Entry(root, width=50)
filename_entry.pack(pady=5)

# Generate Button
tk.Button(root, text="Generate", command=generate_document).pack(pady=20)

root.mainloop()
