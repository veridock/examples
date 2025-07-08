#!/usr/bin/env python3
"""
Setup script dla SVG Browser
Alternatywa dla Poetry - można używać pip install -e .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="svg_browser",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Lokalny serwer do przeglądania plików SVG z kategoryzacją PWA i metadanych",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.3.0",
        "python-dotenv>=1.0.0",
        "lxml>=4.9.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "svg_browser=svg_browser.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "svg_browser": ["templates/*.html"],
    },
)