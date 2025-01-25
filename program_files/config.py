import os

# File Paths
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "program_data")
SETTINGS_FILE = os.path.join(DATA_FILE_PATH, "settings.json")
EXAMPLE_DOCS_FILE = os.path.join(DATA_FILE_PATH, "example_docs.json")
INFORMATION_DOCS_FILE = os.path.join(DATA_FILE_PATH, "information_docs.json")
DEFAULT_DOWNLOAD_DIR = os.path.join(DATA_FILE_PATH, "generated_docs")

# Ensure directories exist
if not os.path.exists(DEFAULT_DOWNLOAD_DIR):
    os.makedirs(DEFAULT_DOWNLOAD_DIR)