from typing import Dict, Any
from ..services.gemini_service import GeminiService
from ..services.web_scraper import WebScraper
from ..utils.logger import setup_logger

logger = setup_logger()

class ProductServiceExtractor:
    def __init__(self, gemini_service: GeminiService, web_scraper: WebScraper = None):
        self.gemini_service = gemini_service
        self.web_scraper = web_scraper
    
    def get_products_services(self, company_name: str) -> Dict[str, Any]:
        """
        Gather information about a company's products and services.
        
        Args:
            company_name (str): Name of the company
            
        Returns:
            dict: Information about products and services
        """
        web_products = []
        web_confidence = "low"
        
        if self.web_scraper:
            try:
                web_info = self.web_scraper.search_company_info(company_name)
                if web_info.get("found_website", False):
                    website_info = web_info.get("website_info", {})
                    web_products = website_info.get("products_services", [])
                    if web_products:
                        web_confidence = "medium"
                        if len(web_products) > 3:
                            web_confidence = "high"
            except Exception as e:
                logger.error(f"Error getting products from website: {e}")
        
        prompt = f"""
        Research the company "{company_name}" and list its main products and services.
        
        Format the response as JSON with these keys:
        1. "products": [list of product names/categories]
        2. "services": [list of service names/categories]
        3. "confidence": (high, medium, or low based on information certainty)
        """
        
        try:
            result = self.gemini_service.generate_response(prompt)
            
            # Merge web-scraped data if available
            if web_products:
                # Add web-scraped products that aren't in the AI results
                ai_products = result.get("products", [])
                ai_services = result.get("services", [])
                
                # Simple function to check if an item is likely already in the list
                def is_duplicate(item, existing_list):
                    item_lower = item.lower()
                    return any(existing.lower() in item_lower or item_lower in existing.lower() 
                              for existing in existing_list)
                
                # Add web scraped products that aren't already included
                for product in web_products:
                    if not is_duplicate(product, ai_products) and not is_duplicate(product, ai_services):
                        # Try to categorize as product or service
                        if any(term in product.lower() for term in ["service", "consulting", "solution", "platform"]):
                            ai_services.append(product)
                        else:
                            ai_products.append(product)
                
                result["products"] = ai_products
                result["services"] = ai_services
                
                # Adjust confidence if necessary
                if result.get("confidence", "low") == "low" and web_confidence in ["medium", "high"]:
                    result["confidence"] = web_confidence
                
                # Add source information
                result["sources"] = ["gemini_api", "company_website"]
            
            return result
        except Exception as e:
            # If AI fails but we have web data, return web data
            if web_products:
                return {
                    "products": web_products,
                    "services": [],
                    "confidence": web_confidence,
                    "sources": ["company_website"],
                    "note": "Retrieved from website due to API error"
                }
            return {"error": str(e), "products": [], "services": [], "confidence": "low"}
