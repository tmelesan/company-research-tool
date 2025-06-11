from typing import Dict, Any
from ..services.gemini_service import GeminiService
from ..services.web_scraper import WebScraper
from ..utils.logger import setup_logger

logger = setup_logger()

class CompanyExistenceChecker:
    def __init__(self, gemini_service: GeminiService, web_scraper: WebScraper = None):
        self.gemini_service = gemini_service
        self.web_scraper = web_scraper
    
    def check_company_exists(self, company_name: str) -> Dict[str, Any]:
        """
        Check if a company exists using Gemini API.
        
        Args:
            company_name (str): Name of the company to check
            
        Returns:
            dict: Information about the company's existence
        """
        prompt = f"""
        I need to verify if a company called "{company_name}" exists. 
        Please provide:
        1. Whether this company likely exists (Yes, No, or Unclear)
        2. A brief reason for your conclusion
        3. What industry it appears to be in (if it exists)
        
        Format your response as JSON with keys: "exists", "reason", "industry"
        """
        
        try:
            result = self.gemini_service.generate_response(prompt)
            
            # If web scraping is enabled, try to find the company's website
            if self.web_scraper and result.get("exists", "").lower() == "yes":
                logger.info(f"Searching for website of {company_name}")
                web_info = self.web_scraper.search_company_info(company_name)
                if web_info.get("found_website", False):
                    result["website_found"] = True
                    result["website"] = web_info.get("url", "")
                    result["domain"] = web_info.get("domain", "")
            
            return result
        except Exception as e:
            return {"exists": "Error", "reason": str(e), "industry": None}
