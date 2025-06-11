import google.generativeai as genai
import os
from typing import Dict, Any, List, Optional
from ..utils.json_helper import extract_json_from_response
from ..utils.logger import setup_logger

logger = setup_logger()

class GeminiService:
    def __init__(self, api_key=None):
        """
        Initialize the Gemini API service.
        
        Args:
            api_key (str, optional): Google Gemini API key
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("No Gemini API key provided. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def generate_response(self, prompt: str) -> Dict[str, Any]:
        """
        Generate a response using the Gemini API.
        
        Args:
            prompt (str): The prompt to send to the API
            
        Returns:
            dict: The parsed JSON response
        """
        try:
            response = self.model.generate_content(prompt)
            return extract_json_from_response(response.text)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {"error": str(e)}
