from typing import Dict, Any
from ..services.gemini_service import GeminiService
from ..services.web_scraper import WebScraper
from ..utils.logger import setup_logger

logger = setup_logger()

class CompanyDataExtractor:
    def __init__(self, gemini_service: GeminiService, web_scraper: WebScraper = None):
        self.gemini_service = gemini_service
        self.web_scraper = web_scraper
    
    def get_company_data(self, company_name: str) -> Dict[str, Any]:
        """
        Gather comprehensive company data using Gemini API and web scraping.
        
        Args:
            company_name (str): Name of the company
            
        Returns:
            dict: Aggregated company data
        """
        # First try to get data from the company website if web scraping is enabled
        website_data = {}
        if self.web_scraper:
            try:
                logger.info(f"Searching for website data for {company_name}")
                web_info = self.web_scraper.search_company_info(company_name)
                if web_info.get("found_website", False):
                    website_data = web_info.get("website_info", {})
                    website_data["data_available"] = True
            except Exception as e:
                logger.error(f"Error getting website data: {e}")
        
        prompt = f"""
        Perform comprehensive research on the company "{company_name}" and provide the following information in JSON format:
        
        1. "company_name": Full official name of the company
        2. "exists": Whether this is a real company (true/false/unclear)
        3. "description": Brief description of what the company does
        4. "industry": Primary industry
        5. "founding_year": When it was founded (if available)
        6. "headquarters": Location of headquarters
        7. "products_services": List of main products and services
        8. "key_people": List of key executives (if available)
        9. "competitors": Major competitors (if available)
        10. "website": Official website URL (if available)
        11. "social_media": Known social media presence
        12. "public_company": Whether it's publicly traded
        13. "stock_symbol": Stock symbol if public
        14. "estimated_size": Approximate company size if known
        15. "data_confidence": Your confidence in this data (high/medium/low)
        
        Include only factual information. If certain information isn't available, use null values.
        """
        
        try:
            result = self.gemini_service.generate_response(prompt)
            
            # Merge with website data if available
            if website_data.get("data_available", False):
                # Update with website information (prefer website data for certain fields)
                if website_data.get("company_name"):
                    result["company_name"] = website_data.get("company_name")
                
                if website_data.get("description"):
                    result["description"] = website_data.get("description")
                
                if website_data.get("website"):
                    result["website"] = website_data.get("website")
                
                # Add website products if missing from API results
                web_products = website_data.get("products_services", [])
                if web_products:
                    api_products = result.get("products_services", [])
                    # Add non-duplicate products
                    for product in web_products:
                        if product not in api_products:
                            api_products.append(product)
                    result["products_services"] = api_products
                
                # Add social media information
                if website_data.get("social_media"):
                    result["social_media"] = {**result.get("social_media", {}), **website_data.get("social_media", {})}
                
                # Add contact info as additional data
                if website_data.get("contact_info"):
                    result["contact_info"] = website_data.get("contact_info")
                
                # Indicate that data includes website information
                result["data_sources"] = ["gemini_api", "company_website"]
            else:
                result["data_sources"] = ["gemini_api"]
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting company data: {e}")
            # If API call fails but we have website data, return a combination of website data
            if website_data.get("data_available", False):
                return {
                    "company_name": website_data.get("company_name", company_name),
                    "exists": True,
                    "description": website_data.get("description", ""),
                    "website": website_data.get("website", ""),
                    "products_services": website_data.get("products_services", []),
                    "social_media": website_data.get("social_media", {}),
                    "contact_info": website_data.get("contact_info", {}),
                    "data_confidence": "medium",
                    "data_sources": ["company_website"],
                    "api_error": str(e)
                }
            return {
                "company_name": company_name,
                "error": str(e),
                "data_confidence": "low"
            }
