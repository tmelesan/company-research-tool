# Moving web_scraper.py content here
from bs4 import BeautifulSoup
import logging
import re
import requests
import trafilatura
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse, urljoin
from ..utils.logger import setup_logger
from ..utils.domain_validator import validate_domain, validate_domain_relevance

logger = setup_logger()

class WebScraper:
    """Class for web scraping operations related to company research."""
    
    def __init__(self, user_agent: str = None, timeout: int = 10):
        """
        Initialize the web scraper with custom options.
        
        Args:
            user_agent (str, optional): Custom User-Agent header for requests.
            timeout (int, optional): Timeout for HTTP requests in seconds.
        """
        self.timeout = timeout
        self.headers = {
            'User-Agent': user_agent or 'Company Research Tool/1.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        # Common page types to search for
        self.page_types = {
            'about': ['about', 'company', 'who-we-are', 'about-us', 'our-story', 'history'],
            'products': ['products', 'services', 'solutions', 'offerings', 'what-we-do'],
            'team': ['team', 'leadership', 'management', 'our-team', 'people'],
            'careers': ['careers', 'jobs', 'work-with-us', 'join-us'],
            'investors': ['investors', 'investor-relations', 'ir', 'shareholders'],
            'blog': ['blog', 'news', 'insights', 'articles', 'press'],
            'contact': ['contact', 'contact-us', 'get-in-touch', 'support']
        }
        # Track the last URL visited (for resolving relative URLs)
        self.last_url = None

    def search_company_info(self, company_name: str) -> Dict[str, Any]:
        """
        Search for company information online.
        
        Args:
            company_name (str): The name of the company to search for
            
        Returns:
            dict: A dictionary containing company information from web sources
        """
        try:
            # Create base response structure
            result = {
                "company_name": company_name,
                "data_found": False,
                "website": None,
                "description": None,
                "products": [],
                "services": [],
                "leadership": [],
                "financials": {},
                "source_urls": []
            }
            
            # Search for company website and basic info
            search_url = f"https://www.google.com/search?q={company_name}+company+official+website"
            response = requests.get(search_url, headers=self.headers, timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract first search result as company website
                search_results = soup.find_all('div', class_='g')
                if search_results:
                    first_result = search_results[0]
                    website_link = first_result.find('a')
                    if website_link:
                        result["website"] = website_link.get('href')
                        result["data_found"] = True
                        result["source_urls"].append(result["website"])
                        
                        # Try to get company description
                        description = first_result.find('div', class_='VwiC3b')
                        if description:
                            result["description"] = description.text.strip()
            
            return result
            
        except Exception as e:
            logger.error(f"Error searching for company info: {e}")
            return {
                "company_name": company_name,
                "data_found": False,
                "error": str(e)
            }
    
    def verify_domain(self, domain: str) -> Dict[str, Any]:
        """
        Verify if a domain is accessible and returns a valid response with detailed status.
        
        Args:
            domain (str): The domain to verify (e.g., 'example.com')
            
        Returns:
            dict: A dictionary containing verification results:
                - exists (bool): True if domain is accessible
                - status (str): Detailed status message
                - https_enabled (bool): True if HTTPS is supported
        """
        try:
            result = {
                "exists": False,
                "status": "",
                "https_enabled": False
            }

            # Basic format validation
            if not domain or not '.' in domain:
                result["status"] = "Invalid domain format"
                return result

            # Clean the domain
            domain = domain.strip().lower()
            if domain.startswith(('http://', 'https://')):
                parsed = urlparse(domain)
                domain = parsed.netloc
            
            # Try HTTPS first
            try:
                response = requests.head(
                    f'https://{domain}',
                    headers=self.headers,
                    timeout=self.timeout,
                    allow_redirects=True
                )
                if response.status_code < 400:
                    result.update({
                        "exists": True,
                        "status": "Domain accessible via HTTPS",
                        "https_enabled": True
                    })
                    return result
            except requests.RequestException:
                # HTTPS failed, try HTTP
                pass
            
            # Try HTTP if HTTPS failed
            try:
                response = requests.head(
                    f'http://{domain}',
                    headers=self.headers,
                    timeout=self.timeout,
                    allow_redirects=True
                )
                if response.status_code < 400:
                    result.update({
                        "exists": True,
                        "status": "Domain accessible via HTTP only",
                        "https_enabled": False
                    })
                    return result
            except requests.RequestException as e:
                result["status"] = f"Domain unreachable: {str(e)}"
                return result
            
            result["status"] = f"Domain returned error status: {response.status_code}"
            return result
            
        except Exception as e:
            logger.debug(f"Error verifying domain {domain}: {str(e)}")
            return {
                "exists": False,
                "status": f"Verification error: {str(e)}",
                "https_enabled": False
            }
