from typing import Dict, Any
from ..services.gemini_service import GeminiService
from ..services.web_scraper import WebScraper
from ..utils.logger import setup_logger

logger = setup_logger()

class LeadershipExtractor:
    def __init__(self, gemini_service: GeminiService, web_scraper: WebScraper = None):
        self.gemini_service = gemini_service
        self.web_scraper = web_scraper
    
    def get_leadership_info(self, company_name: str, domain: str = None) -> Dict[str, Any]:
        """
        Get information about a company's leadership team.
        
        Args:
            company_name (str): Name of the company
            domain (str, optional): Company's website domain if known
            
        Returns:
            dict: Information about the company's leadership team
        """
        if not self.web_scraper:
            return {"error": "Web scraping is disabled", "data_available": False}
            
        try:
            # If domain is provided, use it directly
            if domain:
                logger.info(f"Using provided domain {domain} to extract leadership information")
                website_data = self.web_scraper.extract_from_website(domain)
                
                if "leadership_team" in website_data and website_data["leadership_team"]:
                    return {
                        "data_available": True,
                        "company_name": website_data.get("company_name", company_name),
                        "website": domain,
                        "leadership_team": website_data["leadership_team"]
                    }
            
            # Otherwise search for the company website first
            logger.info(f"Searching for website of {company_name}")
            web_info = self.web_scraper.search_company_info(company_name)
            
            if web_info.get("found_website", False):
                website_info = web_info.get("website_info", {})
                
                if "leadership_team" in website_info and website_info["leadership_team"]:
                    return {
                        "data_available": True,
                        "company_name": website_info.get("company_name", company_name),
                        "website": web_info.get("url"),
                        "leadership_team": website_info["leadership_team"]
                    }
            
            # If we have a website but couldn't find leadership info, try to use Gemini API
            if web_info.get("found_website", False):
                prompt = f"""
                Research the leadership team of {company_name} (website: {web_info.get("url")}).
                Please provide information about:
                1. The CEO/Managing Director
                2. Other key executives (CFO, CTO, COO, etc.)
                3. Board members (if applicable)
                
                Format your response as JSON with an array of 'executives', each containing:
                {{"name": "Executive Name", "title": "Position/Title", "background": "Brief background if available"}}
                """
                
                leaders = self.gemini_service.generate_response(prompt)
                
                if "executives" in leaders and leaders["executives"]:
                    return {
                        "data_available": True,
                        "company_name": company_name,
                        "website": web_info.get("url"),
                        "leadership_team": leaders["executives"],
                        "source": "AI generated"
                    }
            
            # Fall back to just Gemini API with no website context
            prompt = f"""
            Research the leadership team of {company_name}.
            Please provide information about:
            1. The CEO/Managing Director
            2. Other key executives (CFO, CTO, COO, etc.)
            3. Board members (if applicable)
            
            Format your response as JSON with an array of 'executives', each containing:
            {{"name": "Executive Name", "title": "Position/Title", "background": "Brief background if available"}}
            """
            
            leaders = self.gemini_service.generate_response(prompt)
            
            leadership_team = []
            # Check if leaders is a dictionary with 'executives' key
            if isinstance(leaders, dict) and "executives" in leaders:
                leadership_team = leaders["executives"]
            # Check if leaders itself is a list (direct array response)
            elif isinstance(leaders, list):
                leadership_team = leaders
            
            return {
                "data_available": True if leadership_team else False,
                "company_name": company_name,
                "leadership_team": leadership_team,
                "source": "AI generated"
            }
            
        except Exception as e:
            logger.error(f"Error getting leadership information: {e}")
            return {
                "data_available": False, 
                "error": str(e)
            }
