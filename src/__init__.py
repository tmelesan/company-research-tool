"""
Company Research Tool

A comprehensive Python tool for researching companies using Google's Gemini AI 
and web scraping technologies.
"""

import os

# Read version from VERSION file
def get_version():
    """Get the current version of the package."""
    version_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION')
    try:
        with open(version_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "2.1.0"  # Fallback version

__version__ = get_version()
__author__ = "Konstantinos"
__email__ = "your-email@example.com"
__description__ = "🔍 Comprehensive AI-powered company research tool with web interface using Google Gemini AI and web scraping"

from .company_researcher import CompanyResearcher

__all__ = ['CompanyResearcher', '__version__']
