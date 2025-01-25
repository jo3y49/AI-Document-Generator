import tkinter as tk
from document_handler import (
    upload_example_docs,
    upload_information_docs,
    generate_document,
    clear_example,
    clear_all_examples,
    clear_information,
    clear_all_information,
    get_example_docs,
    get_information_docs
)
from settings import set_download_path, save_settings

def create_ui(settings):
    """Create the main UI for the document generator application."""
    root = tk.Tk()

    # Create the main window
    root.title("Document Generator")

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set window size to 60% of screen width and 80% of screen height
    window_width = int(screen_width * 0.6)
    window_height = int(screen_height * 0.8)

    # Center the window on the screen
    position_x = (screen_width - window_width) // 2
    position_y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

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
    download_path_entry.insert(0, settings.get("download_path"))
    download_path_entry.bind("<Button-1>", lambda: set_download_path(download_path_entry=download_path_entry, settings=settings))
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

    def show_uploaded_files(root):
        """Show a popup with the filenames of all uploaded documents."""
        example_doc_dict = get_example_docs()
        information_doc_dict = get_information_docs()
        popup = tk.Toplevel(root)
        popup.title("Uploaded Files")

        # Get dimensions of the root window
        root.update_idletasks()
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        # Scale popup size based on main window dimensions (e.g., 70% of width, 60% of height)
        popup_width = int(root_width * 0.7)
        popup_height = int(root_height * 0.6)

        # Ensure minimum size for usability
        popup_width = max(popup_width, 500)
        popup_height = max(popup_height, 400)

        # Calculate center position relative to the root window
        position_x = root_x + (root_width // 2) - (popup_width // 2)
        position_y = root_y + (root_height // 2) - (popup_height // 2)

        popup.geometry(f"{popup_width}x{popup_height}+{position_x}+{position_y}")

        def delete_selected_from_listbox(listbox, doc_dict):
            if doc_dict is example_doc_dict:
                clear_func = clear_example
            elif doc_dict is information_doc_dict:
                clear_func = clear_information
            else:
                return

            selected_indices = listbox.curselection()
            if not selected_indices:
                return
            
            for index in selected_indices:
                filename = listbox.get(index)
                listbox.delete(index)
                doc_dict = clear_func(filename)

        def clear_docs(listbox, doc_dict):
            if doc_dict is example_doc_dict:
                clear_func = clear_all_examples
            elif doc_dict is information_doc_dict:
                clear_func = clear_all_information
            else:
                return

            listbox.delete(0, tk.END)
            doc_dict = clear_func()

        # Example Documents
        tk.Label(popup, text="Example Documents:").pack(anchor="center", padx=10, pady=5)
        example_listbox = tk.Listbox(popup, width=50, selectmode=tk.MULTIPLE)
        example_listbox.pack(padx=10, pady=5)
        for filename in example_doc_dict.keys():
            example_listbox.insert(tk.END, filename)
        example_button_frame = tk.Frame(popup)
        example_button_frame.pack(pady=5)
        tk.Button(
            example_button_frame, text="Delete Selected", 
            command=lambda: delete_selected_from_listbox(example_listbox, example_doc_dict)
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(example_button_frame, text="Clear All", command=lambda: clear_docs(example_listbox, example_doc_dict)).pack(side=tk.LEFT, padx=5)

        # Informational Documents
        tk.Label(popup, text="Informational Documents:").pack(anchor="center", padx=10, pady=5)
        info_listbox = tk.Listbox(popup, width=50, selectmode=tk.MULTIPLE)
        info_listbox.pack(padx=10, pady=5)
        for filename in information_doc_dict.keys():
            info_listbox.insert(tk.END, filename)
        info_button_frame = tk.Frame(popup)
        info_button_frame.pack(pady=5)
        tk.Button(
            info_button_frame, text="Delete Selected", 
            command=lambda: delete_selected_from_listbox(info_listbox, information_doc_dict)
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(info_button_frame, text="Clear All", command=lambda: clear_docs(info_listbox, information_doc_dict)).pack(side=tk.LEFT, padx=5)

        # Close Button
        tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

        popup.transient(root)  # Set the popup as a transient window for the root
        popup.grab_set()  # Disable interaction with the root window
        root.wait_window(popup)  # Wait until the popup is closed before continuing

    # Show Uploaded Files Button
    tk.Button(root, text="Show Uploaded Documents", command=lambda: show_uploaded_files(root=root)).pack(pady=5)

    return root