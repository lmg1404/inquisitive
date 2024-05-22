""" 
What this does is goes through every directory and looks for a __init__.py
Treats it all as a local package

we then just have to do pip install -r requirements.txt
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    
__version__ = "0.0.0" # code provisioning

REPO_NAME = "inquisitive"
AUTHOR_USER_NAME = "lmg1404"
SRC_REPO = "package"
AUTHOR_EMAIL = "luismg0203@gmail.com"
    
setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="RAG app which asks questions based on documents uploaded for comprehension.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"",
    project_urls={
        "Bug Tracker": f""
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)