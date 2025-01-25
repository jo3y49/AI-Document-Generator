import tkinter as tk
from document_handler import load_docs
from settings import load_settings
from interface import create_ui

def setup():
    load_docs()
    settings = load_settings()
    root = create_ui(settings)
    return root

root = setup()
root.mainloop()