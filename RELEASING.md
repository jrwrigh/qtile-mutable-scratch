# Steps for Release

0. Update version in `_version.py`
1. Build the wheels via `hatch build`
    - This will create files in a directory called `dist`
2. Upload the wheels to PyPI via `hatch publish`
    - This will require an API token to perform the upload
        - Username is `__token__`, password is the token itself
