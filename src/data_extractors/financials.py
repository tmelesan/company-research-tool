from typing import Dict, Any
from ..services.gemini_service import GeminiService
from ..services.web_scraper import WebScraper
from ..utils.logger import setup_logger

logger = setup_logger()

class CompanyFinancialsExtractor:
    def __init__(self, gemini_service: GeminiService, web_scraper: WebScraper = None):
        self.gemini_service = gemini_service
        self.web_scraper = web_scraper
    
    def get_financials(self, company_name: str, domain: str = None) -> Dict[str, Any]:
        """
        Get financial information about a company.
        
        Args:
            company_name (str): Name of the company
            domain (str, optional): Company's website domain if known
            
        Returns:
            dict: Financial information about the company
        """
        try:
            result = {
                "data_available": False,
                "company_name": company_name,
                "financial_information": {}
            }
            
            # First try web scraping if enabled
            if self.web_scraper:
                # If domain is provided, use it directly
                if domain:
                    logger.info(f"Using provided domain {domain} to extract financial information")
                    website_data = self.web_scraper.extract_from_website(domain)
                    
                    if "financial_information" in website_data and any(website_data["financial_information"].values()):
                        result["data_available"] = True
                        result["website"] = domain
                        result["financial_information"] = website_data["financial_information"]
                        result["source"] = "website"
                else:
                    # Search for the company website
                    logger.info(f"Searching for website of {company_name}")
                    web_info = self.web_scraper.search_company_info(company_name)
                    
                    if web_info.get("found_website", False):
                        website_info = web_info.get("website_info", {})
                        
                        if "financial_information" in website_info and any(website_info["financial_information"].values()):
                            result["data_available"] = True
                            result["website"] = web_info.get("url")
                            result["financial_information"] = website_info["financial_information"]
                            result["source"] = "website"
            
            # If web scraping didn't yield results, use Gemini API
            if not result["data_available"]:
                # Check if the company is publicly traded
                prompt = f"""
                Is {company_name} a publicly traded company? If so, provide:
                1. Stock symbol/ticker
                2. Stock exchange(s) it's listed on
                3. Approximate market capitalization (if available)
                
                Format your response as JSON with keys: "is_public", "symbol", "exchange", "market_cap"
                """
                
                public_info = self.gemini_service.generate_response(prompt)
                
                # If it's a public company, get more financial information
                is_public_value = public_info.get("is_public")
                is_public = False
                
                # Handle different ways the API might return "is_public" (string or boolean)
                if isinstance(is_public_value, bool):
                    is_public = is_public_value
                elif isinstance(is_public_value, str):
                    is_public = is_public_value.lower() in ["yes", "true", "1"]
                
                if is_public:
                    prompt = f"""
                    Provide REAL financial information about {company_name} (ticker: {public_info.get("symbol", "")}). 
                    DO NOT use placeholder or template data. Only include actual financial figures if you know them.
                    
                    Please provide:
                    1. Latest quarterly revenue and profit (in actual USD amounts)
                    2. Key financial ratios (actual values only)
                    3. Recent financial news headlines (real news, not placeholders)
                    
                    Format as JSON:
                    {{
                        "company": "{company_name}",
                        "ticker": "actual_ticker_symbol",
                        "lastUpdated": "YYYY-MM-DD or period",
                        "financials": {{
                            "revenue": {{
                                "latestQuarter": {{
                                    "value": actual_number_in_usd,
                                    "period": "Q1 2024 or actual period",
                                    "currency": "USD"
                                }}
                            }},
                            "profit": {{
                                "latestQuarter": {{
                                    "value": actual_number_in_usd,
                                    "period": "Q1 2024 or actual period", 
                                    "currency": "USD"
                                }}
                            }},
                            "keyRatios": {{
                                "peRatio": {{"value": actual_number, "asOfDate": "YYYY-MM-DD"}},
                                "eps": {{"value": actual_number, "asOfDate": "YYYY-MM-DD"}}
                            }}
                        }},
                        "recentNews": [
                            {{
                                "headline": "Real news headline here",
                                "source": "Actual source name",
                                "date": "YYYY-MM-DD"
                            }}
                        ]
                    }}
                    
                    IMPORTANT: Only include data you are confident about. If you don't have real data for a field, set it to null or omit it entirely. Do not use placeholder text.
                    """
                    
                    financial_data = self.gemini_service.generate_response(prompt)
                    
                    result["data_available"] = True
                    result["financial_information"] = financial_data  # Use the structured response directly
                    result["source"] = "Gemini AI"
                else:
                    # For private companies, try to get some general financial information
                    prompt = f"""
                    Provide any REAL, publicly available financial information about {company_name}.
                    DO NOT use placeholder data. Only include information you are confident about.
                    
                    This may include:
                    1. Estimated revenue (if publicly disclosed)
                    2. Funding rounds and valuations (if it's a startup with disclosed funding)
                    3. Employee count or company size indicators
                    4. Recent financial news or developments
                    
                    Format as JSON:
                    {{
                        "company": "{company_name}",
                        "companyType": "private",
                        "financials": {{
                            "estimatedRevenue": {{"value": actual_number_if_known, "year": "YYYY", "source": "source_name"}},
                            "funding": {{
                                "totalFunding": actual_amount_if_known,
                                "lastRound": {{"amount": amount, "date": "YYYY-MM-DD", "type": "Series A/B/etc"}}
                            }},
                            "employees": actual_count_if_known
                        }},
                        "recentNews": [
                            {{
                                "headline": "Real news headline",
                                "source": "Actual source",
                                "date": "YYYY-MM-DD"
                            }}
                        ]
                    }}
                    
                    IMPORTANT: Only include data you have confidence in. If you don't have real data, set fields to null or omit them. Do not use placeholder text.
                    """
                    
                    financial_data = self.gemini_service.generate_response(prompt)
                    
                    result["data_available"] = True
                    result["financial_information"] = financial_data  # Use structured response directly
                    result["source"] = "Gemini AI"
            
            return result
                
        except Exception as e:
            logger.error(f"Error getting financial information: {e}")
            return {
                "data_available": False, 
                "error": str(e),
                "company_name": company_name
            }
