import pdb  # Python debugger
from typing import Dict, Any, Union, List, Optional
from ..services.gemini_service import GeminiService
from ..services.web_scraper import WebScraper
from ..utils.domain_validator import validate_domain, validate_domain_relevance
from ..utils.logger import setup_logger, debug_print
from ..utils.cache_manager import CacheManager

logger = setup_logger()

class CompanyExistenceChecker:
    def __init__(self, gemini_service: GeminiService, web_scraper: WebScraper = None, cache_ttl: int = 86400):
        self.gemini_service = gemini_service
        self.web_scraper = web_scraper
        self.cache_manager = CacheManager(cache_dir=".cache/company_existence", default_ttl=cache_ttl)
        
    def _debug_domain_validation(self, domain: str, validation_result: Dict[str, Any]):
        """Helper method to debug domain validation results"""
        debug_print({
            'domain': domain,
            'validation': validation_result
        }, f"Domain Validation Results for {domain}")
    
    def check_company_exists(self, company_name: str, domains: Union[str, List[str]] = None) -> Dict[str, Any]:
        """
        Check if a company exists using Gemini API and verify domains.
        Includes built-in debugging support.
        
        Args:
            company_name (str): Name of the company to check
            domains (Union[str, List[str]], optional): Company's website domain(s) to verify
            
        Returns:
            Dict[str, Any]: Results of company existence check and domain validation
        
        Debug Tips:
        - Set breakpoint using: import pdb; pdb.set_trace()
        - Use debug_print() for complex data structures
        - Check logger output for detailed validation steps
        """
        # Check cache first
        cache_key = {
            'company_name': company_name,
            'domains': domains if isinstance(domains, (list, type(None))) else [domains]
        }
        
        cached_result = self.cache_manager.get('existence_check', cache_key)
        if cached_result:
            debug_print(cached_result, "Cache hit: Using cached result")
            return cached_result
            
        # If not in cache, proceed with normal check
        try:
            # Debug: Initial parameters
            debug_print({
                'company_name': company_name,
                'domains': domains
            }, "Company Existence Check - Initial Parameters")

            # Convert single domain to list for consistent processing
            # Domains must be provided as an argument; do not fetch from scraper
            if domains is None:
                logger.warning("No domains provided to check_company_exists; expected domains as argument from caller.")
                domain_list = []
            elif isinstance(domains, str):
                domain_list = [domains]
            else:
                domain_list = domains

            # Ensure domains are not fetched from the web scraper
            assert self.web_scraper is None or not hasattr(self.web_scraper, "fetch_domains"), (
                "Domains must be provided by the caller, not fetched from the scraper."
            )
              # Validate each domain
            domain_validations = {}
            for domain in domain_list:
                is_valid, validation_msg = validate_domain(domain)
                validation_result = {
                    'is_valid': is_valid,
                    'status_message': validation_msg
                }
                
                relevance_result = None
                if is_valid:
                    is_relevant, relevance_msg = validate_domain_relevance(domain, company_name)
                    relevance_result = {
                        'is_relevant': is_relevant,
                        'status_message': relevance_msg
                    }
                
                domain_validations[domain] = {
                    'validation': validation_result,
                    'relevance': relevance_result
                }
                  # Debug: Domain validation results
                self._debug_domain_validation(domain, domain_validations[domain])
                
                # Optional debugging breakpoint
                # Uncomment to debug specific domains:
                # if domain == "example.com":
                #     pdb.set_trace()
              # Process Gemini response
            domain_info = f"with domains: {', '.join(domain_list)}" if domain_list else "without any provided domains"
            prompt = f"""
            Analyze if the company "{company_name}" exists {domain_info}.

            Look for these aspects:
            1. Company existence verification
            2. Industry identification
            3. Business legitimacy assessment
            
            Respond in this exact JSON format:
            {{
                "exists": "Yes/No/Unclear",
                "reason": "Brief explanation of your conclusion",
                "industry": "Industry name if known, or null"
            }}
            """
            
            try:
                gemini_response = self.gemini_service.generate_response(prompt)
                # Debug: Gemini response
                debug_print(gemini_response, "Raw Gemini API Response")
                
                # Ensure we have valid response format
                if not isinstance(gemini_response, dict) or "error" in gemini_response:
                    logger.error(f"Invalid Gemini response: {gemini_response}")
                    gemini_response = {
                        "exists": "Unclear",
                        "reason": "Could not verify company existence",
                        "industry": None
                    }
            except Exception as e:
                logger.error(f"Error processing Gemini response: {e}")
                gemini_response = {
                    "exists": "Error",
                    "reason": str(e),
                    "industry": None
                }
                
            # Debug: Processed response
            debug_print(gemini_response, "Processed Gemini Response")
              # Calculate existence based on both domain validation and Gemini response
            domain_exists = any(
                v.get('validation', {}).get('is_valid', False) 
                for v in domain_validations.values()
            ) if domain_validations else None

            gemini_exists = None
            if gemini_response.get("exists"):
                gemini_exists = {
                    "yes": True,
                    "no": False
                }.get(gemini_response.get("exists", "").lower())

            # Determine final existence status
            exists = None
            if domain_exists is not None and gemini_exists is not None:
                exists = domain_exists and gemini_exists
            elif domain_exists is not None:
                exists = domain_exists
            else:
                exists = gemini_exists

            result = {
                'company_name': company_name,
                'domains': domain_validations,
                'domain_validation': {
                    'exists': domain_exists,
                    'valid_domains': [
                        domain for domain, data in domain_validations.items()
                        if data.get('validation', {}).get('is_valid', False)
                    ] if domain_validations else []
                },
                'gemini_response': gemini_response,
                'exists': exists,
                'confidence': 'high' if domain_exists and gemini_exists is not None else 'medium' if domain_exists or gemini_exists is not None else 'low'
            }
            
            # Final debug output
            debug_print(result, "Final Check Results")
            
            # Cache the result before returning
            self.cache_manager.set('existence_check', cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Error in company existence check: {str(e)}")
            debug_print(str(e), "Error in company_exists check")
            raise
