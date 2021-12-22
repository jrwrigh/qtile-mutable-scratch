import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qtile-mutable_scratch",
    version="0.0.1",
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
    py_modules = ['MutableScratch'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
