#!/bin/bash

# Company Research Tool CLI - Secure API Key Runner
echo "Please enter your Google Gemini API key:"
read -s GEMINI_API_KEY
export GEMINI_API_KEY

echo "API key set. Running CLI command..."
python cli.py "$@"
