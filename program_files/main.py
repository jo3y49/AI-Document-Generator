import tkinter as tk
from document_handler import load_docs
from settings import load_settings
from interface import create_ui
    
load_docs()
settings = load_settings()

root = tk.Tk()
root = create_ui(root, settings)
root.mainloop()