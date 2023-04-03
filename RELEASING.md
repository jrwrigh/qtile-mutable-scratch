# Steps for Release

0. Update version in `setup.py`
1. Build the wheels via `python -m build`
    - This will create files in a directory called `dist`
2. Upload the wheels to PyPI via `twine`
    - `python3 -m twine upload dist/*`
    - This will require an API token to perform the upload
