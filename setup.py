import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("qtile_mutable_scratch/_version.py", "r") as fh:
    line = fh.read()
exec(line)

setuptools.setup(
    name="qtile-mutable_scratch",
    version=__version__,
    author="James Wright",
    author_email="james@jameswright.xyz",
    description="Add mutable scratch functionality to qtile",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrwrigh/qtile-mutable_scratch",
    project_urls={
        "Bug Tracker": "https://github.com/jrwrigh/qtile-mutable_scratch/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="./qtile_mutable_scratch"),
    python_requires=">=3.6",
)
