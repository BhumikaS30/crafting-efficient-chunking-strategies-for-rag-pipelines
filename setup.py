from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    Returns the list of dependencies required by the project.
    """
    return [
        "argparse",
        "numpy",
        "pandas",
        "torch",
        "transformers",
    ]

def get_long_description() -> str:
    """
    Returns the long description of the project.
    """
    with open("README.md", "r") as f:
        return f.read()

setup(
    name="crafting-efficient-chunking-strategies",
    version="1.0.0",
    description="A Python script for crafting efficient chunking strategies for RAG pipelines",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/your-username/crafting-efficient-chunking-strategies",
    packages=find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "main=main:main",
        ],
    },
)