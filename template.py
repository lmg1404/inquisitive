"""
Why are we making this?
- Instead of making a bunch of files manually we can just have this program that does it for us
- Really one time effort so we don't have to do it again
"""

import os
from pathlib import Path 
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = 'inquisitive'

list_of_files = [
    ".github/workflows/.gitkeep",
    "app/__init__.py",
    "app/main.py",
    "app/api/__init__.py",
    "app/api/endpoints/__init__.py",
    "app/api/endpoints/pdf_processing.py",
    "app/api/endpoints/statistics.py",
    "app/core/__init__.py",
    "app/core/config.py",
    "app/models/__init__.py",
    "app/services/__init__.py",
    "app/services/pdf_extraction.py",
    "app/services/nlp_processing.py",
    "app/services/chart_generation.py",
    "app/templates/index.html",
    "app/static/css/style.css",
    "app/static/js/script.js",
    "data/raw/",
    "data/processed/",
    "data/external",
    "notebooks/eda/eda.ipynb",
    "notebooks/training/training.ipynb",
    "scripts/data_cleaning.py",
    "scripts/train_model.py",
    "tests/__init__.py",
    "tests/test_api.py",
    "tests/test_services.py",
    "requirements.txt",
    "README.md",
    "Dockerfile",
    "config.yaml",
    ".gitignore",
    "setup.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for file: {filename}")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")