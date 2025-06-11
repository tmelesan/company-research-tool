#!/usr/bin/env python3
"""
Setup script for Company Research Tool
"""

from setuptools import setup, find_packages
import os

# Read version from VERSION file
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    with open(version_file, 'r') as f:
        return f.read().strip()

# Read README for long description
def get_long_description():
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_file, 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="company-research-tool",
    version=get_version(),
    author="Konstantinos",
    author_email="your-email@example.com",
    description="🔍 Comprehensive AI-powered company research tool with web interface using Google Gemini AI and web scraping",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/kpapap/company-research-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "google-generativeai>=0.3.0",
        "argparse>=1.4.0",
        "streamlit>=1.27.0",
        "beautifulsoup4>=4.9.3",
        "requests>=2.25.1",
        "trafilatura>=1.6.0",
        "lxml>=4.9.0",
        "pandas>=1.5.0",
        "plotly>=5.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ]
    },
    entry_points={
        "console_scripts": [
            "company-research=cli:main",
        ],
    },
    keywords=[
        "company research",
        "business intelligence", 
        "ai",
        "gemini",
        "web scraping",
        "streamlit",
        "financial data",
        "competitive analysis"
    ],
    project_urls={
        "Bug Reports": "https://github.com/kpapap/company-research-tool/issues",
        "Source": "https://github.com/kpapap/company-research-tool",
        "Documentation": "https://github.com/kpapap/company-research-tool#readme",
    },
)
