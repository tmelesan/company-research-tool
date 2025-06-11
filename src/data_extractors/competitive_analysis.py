from typing import Dict, Any
from ..services.gemini_service import GeminiService
from ..utils.logger import setup_logger

logger = setup_logger()

class CompetitiveAnalysisExtractor:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
    
    def get_competitive_analysis(self, company_name: str) -> Dict[str, Any]:
        """
        Get competitive analysis for a company.
        
        Args:
            company_name (str): Name of the company
            
        Returns:
            dict: Competitive analysis data
        """
        prompt = f"""
        Perform a competitive analysis for the company "{company_name}". 
        Provide the following information in JSON format:
        
        1. "main_competitors": List of 3-5 main competitors
        2. "market_position": Company's position in the market 
        3. "strengths": Key strengths compared to competitors
        4. "weaknesses": Potential weaknesses compared to competitors
        5. "market_trends": Recent trends in the industry
        6. "data_confidence": Your confidence in this analysis (high/medium/low)
        """
        
        try:
            result = self.gemini_service.generate_response(prompt)
            return result
        except Exception as e:
            return {"error": str(e), "data_confidence": "low"}
