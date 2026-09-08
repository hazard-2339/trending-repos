from pathlib import Path

from setuptools import find_packages, setup


setup(
    name="github-trending",
    version="0.1.0",
    description="Find and display trending GitHub repositories.",
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={"console_scripts": ["github-trending=github_trending.cli:main"]},
)
