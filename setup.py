import io
import os
from setuptools import setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely."""
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    """Parse requirements from a requirements file."""
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="word_counter",
    version=read(
        "word_counter_py", "VERSION"
    ),  # Dynamically read the version from a VERSION file in the word_counter_py folder
    description="A simple command-line tool to count words in a text file and store the result in a SQLite database.",
    long_description=read("README.md"),  # Read README for long description
    long_description_content_type="text/markdown",
    url="https://github.com/Reby0217/ids706-miniProj8",
    author="Kejia Liu",
    py_modules=["cli"],  # Instead of find_packages, use py_modules for single module
    package_dir={"": "word_counter_py"},
    install_requires=read_requirements(
        "requirements.txt"
    ),  # Read dependencies from requirements.txt
    entry_points={
        "console_scripts": [
            "word_counter = cli:main",  # Full module path for cli.py
        ],
    },
    extras_require={
        "test": read_requirements("requirements.txt"),  # Same requirements for testing
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
