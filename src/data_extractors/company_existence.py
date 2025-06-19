from typing import Dict, Any, Union, List, Optional
from ..services.gemini_service import GeminiService
from ..services.web_scraper import WebScraper
from ..utils.logger import setup_logger

logger = setup_logger()

class CompanyExistenceChecker:
    def __init__(self, gemini_service: GeminiService, web_scraper: WebScraper = None):
        self.gemini_service = gemini_service
        self.web_scraper = web_scraper
    
    def check_company_exists(self, company_name: str, domains: Union[str, List[str]] = None) -> Dict[str, Any]:
        """
        Check if a company exists using Gemini API and optionally verify domains.
        
        Args:
            company_name (str): Name of the company to check
            domains (Union[str, List[str]], optional): Company's website domain(s) to verify
            
        Returns:
            Dict[str, Any]: A dictionary containing:
                - company_name: Name of the company checked
                - exists: Whether the company exists (True/False/"Error")
                - reason: Explanation of the existence determination
                - industry: Company's industry if found
                - domains_verified: List of all checked domains with their verification status
                - related_domains: List of domains confirmed to be related to the company
                - unrelated_domains: List of domains found to be unrelated or suspicious
            Returns:
            dict: Information about the company's existence and domain verification
        """        # Convert single domain to list for consistent handling
        if isinstance(domains, str):
            domains = [domains]
            
        result = {
            "company_name": company_name,
            "exists": False,
            "reason": "",
            "industry": "",
            "domains_verified": [],
            "unrelated_domains": [],  # List of domains found to be unrelated
            "related_domains": []     # List of domains confirmed to be related
        }

        # First, check company existence using Gemini
        prompt = f"""
        I need to verify if a company called "{company_name}" exists. 
        Please provide:
        1. Whether this company likely exists (Yes, No, or Unclear)
        2. A brief reason for your conclusion
        3. What industry it appears to be in (if it exists)
        
        Format your response as JSON with keys: "exists", "reason", "industry"
        """
        try:
            gemini_result = self.gemini_service.generate_response(prompt)
            result.update(gemini_result)
            
            # If web scraping is enabled, verify domains
            if self.web_scraper and domains:
                logger.info(f"Verifying domains for {company_name}: {domains}")
                for domain in domains:
                    try:
                        domain_info = {
                            "domain": domain,
                            "verified": False,
                            "status": "inaccessible",
                            "company_related": False,
                            "confidence": "low"
                        }
                        
                        # First verify if domain is accessible
                        if self.web_scraper.verify_domain(domain):
                            domain_info["verified"] = True
                            domain_info["status"] = "accessible"                            # Now check if domain is related to the company
                            verify_prompt = f"""
                            Strictly analyze if the domain "{domain}" is legitimately related to the company "{company_name}".
                            
                            Follow these validation steps and provide detailed analysis:
                            1. Direct name comparison:
                               - Check if company name or its parts are present in the domain
                               - Identify any misspellings or variations
                               - Calculate similarity score between company name and domain
                            
                            2. Brand verification:
                               - Look for known brand names, products, or services of {company_name}
                               - Check for subsidiary or parent company names
                               - Verify legitimate business associations
                            
                            3. Risk assessment:
                               - Flag any suspicious patterns or typosquatting attempts
                               - Identify potential phishing or misleading domains
                               - Check for common domain squatting patterns
                               - Look for intentionally confusing similarities
                            
                            4. Validation rules:
                               - Domain must contain company name or known brand
                               - No suspicious character substitutions
                               - Follow standard corporate domain patterns
                               - Must not be a common phishing pattern
                            
                            Return your analysis as JSON with these keys:
                            - "is_related": false unless domain passes ALL validation rules
                            - "confidence": "high"/"medium"/"low"
                            - "relationship_type": "direct" (exact match), "brand" (related brand/product), "subsidiary", or "unrelated"
                            - "warning": any potential concerns about misleading similarities
                            - "reason": detailed explanation of the relationship or lack thereof
                            """
                            domain_analysis = self.gemini_service.generate_response(verify_prompt)
                            if isinstance(domain_analysis, dict):
                                is_related = domain_analysis.get("is_related", False)
                                domain_info["company_related"] = is_related
                                domain_info["confidence"] = domain_analysis.get("confidence", "low")
                                domain_info["relationship_type"] = domain_analysis.get("relationship_type", "unrelated")
                                domain_info["relation_reason"] = domain_analysis.get("reason", "No analysis available")
                                domain_info["warning"] = domain_analysis.get("warning", "Domain appears unrelated to the company")
                                domain_info["validation_failed"] = not is_related
                                domain_info["risk_level"] = domain_analysis.get("risk_level", "medium")
                                
                                # Add to appropriate list based on relationship
                                if is_related:
                                    result["related_domains"].append({
                                        "domain": domain,
                                        "relationship_type": domain_info["relationship_type"],
                                        "confidence": domain_info["confidence"],
                                        "reason": domain_info["relation_reason"]
                                    })
                                else:
                                    # Enhanced unrelated domain info
                                    result["unrelated_domains"].append({
                                        "domain": domain,
                                        "warning": domain_info["warning"],
                                        "reason": domain_info["relation_reason"],
                                        "risk_level": domain_info["risk_level"],
                                        "validation_message": "⚠️ This domain failed validation checks and appears unrelated to the company.",
                                        "recommendations": [
                                            "Verify the domain is correct",
                                            "Check for typos or misspellings",
                                            "Ensure this is an official company domain",
                                            "Be cautious of potential phishing attempts"
                                        ]
                                    })
                                    
                                    # Log warning for unrelated domains
                                    logger.warning(f"Validation Failed: Domain '{domain}' appears unrelated to company '{company_name}'. "
                                                 f"Reason: {domain_info['relation_reason']}")
                            
                        result["domains_verified"].append(domain_info)
                        
                    except Exception as e:
                        logger.error(f"Error verifying domain {domain}: {e}")
                        error_info = {
                            "domain": domain,
                            "verified": False,
                            "status": f"error: {str(e)}",
                            "company_related": False,
                            "confidence": "low",
                            "relationship_type": "unknown",
                            "reason": "Could not analyze due to error"
                        }
                        result["domains_verified"].append(error_info)
                        result["unrelated_domains"].append({
                            "domain": domain,
                            "warning": "Domain verification failed",
                            "reason": f"Could not analyze due to error: {str(e)}"
                        })
            
            return result
            
        except Exception as e:
            logger.error(f"Error checking company existence for {company_name}: {e}")
            return {
                "company_name": company_name,
                "exists": "Error",
                "reason": str(e),
                "industry": None,
                "domains_verified": []
            }
