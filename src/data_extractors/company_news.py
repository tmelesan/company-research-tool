from typing import Dict, Any
from ..services.gemini_service import GeminiService
from ..utils.logger import setup_logger

logger = setup_logger()

class CompanyNewsExtractor:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
    
    def get_company_news(self, company_name: str, limit: int = 5) -> Dict[str, Any]:
        """
        Get recent news about the company.
        
        Args:
            company_name (str): Name of the company
            limit (int): Maximum number of news items to return
            
        Returns:
            dict: Recent news about the company
        """
        prompt = f"""
        Find recent notable news about "{company_name}". 
        
        Provide the following in JSON format:
        1. "news_items": List of {limit} most significant recent news items, each with:
           - "title": News headline
           - "summary": Brief summary 
           - "date": Approximate date
           - "topic": Category (financial, product, leadership, etc.)
        2. "data_confidence": Your confidence in this data (high/medium/low)
        """
        
        try:
            result = self.gemini_service.generate_response(prompt)
            return result
        except Exception as e:
            return {"error": str(e), "news_items": [], "data_confidence": "low"}
