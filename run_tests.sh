#!/bin/bash

# Set API key for testing
echo "Please enter your Google Gemini API key:"
read -s GEMINI_API_KEY
export GEMINI_API_KEY

echo "API key set. Running tests..."
python -m pytest tests/test_company_researcher.py -v
