from typing import Dict, Any, Optional
from .services.gemini_service import GeminiService
from .services.web_scraper import WebScraper
from .services.financial_service import FinancialService
from .data_extractors.company_existence import CompanyExistenceChecker
from .data_extractors.products_services import ProductServiceExtractor
from .data_extractors.leadership import LeadershipExtractor
from .data_extractors.company_news import CompanyNewsExtractor
from .data_extractors.competitive_analysis import CompetitiveAnalysisExtractor
from .data_extractors.financials import CompanyFinancialsExtractor
from .data_extractors.company_data import CompanyDataExtractor
from .utils.logger import setup_logger

logger = setup_logger()

class CompanyResearcher:
    def __init__(self, api_key=None, use_web_scraping=True, alpha_vantage_key=None):
        """
        Initialize the company researcher tool with Google Gemini API.
        
        Args:
            api_key (str, optional): Google Gemini API key
            use_web_scraping (bool): Whether to use web scraping for additional information
            alpha_vantage_key (str, optional): Alpha Vantage API key for financial data
        """
        # Initialize services
        self.gemini_service = GeminiService(api_key)
        self.web_scraper = WebScraper() if use_web_scraping else None
        self.financial_service = FinancialService(alpha_vantage_key)
        
        # Initialize data extractors
        self.existence_checker = CompanyExistenceChecker(self.gemini_service, self.web_scraper)
        self.product_service_extractor = ProductServiceExtractor(self.gemini_service, self.web_scraper)
        self.leadership_extractor = LeadershipExtractor(self.gemini_service, self.web_scraper)
        self.news_extractor = CompanyNewsExtractor(self.gemini_service)
        self.competitive_analyzer = CompetitiveAnalysisExtractor(self.gemini_service)
        self.financials_extractor = CompanyFinancialsExtractor(self.gemini_service, self.web_scraper, self.financial_service)
        self.data_extractor = CompanyDataExtractor(self.gemini_service, self.web_scraper)
    
    def check_company_exists(self, company_name: str) -> Dict[str, Any]:
        """
        Check if a company exists using Gemini API.
        """
        return self.existence_checker.check_company_exists(company_name)
    
    def get_company_products_services(self, company_name: str) -> Dict[str, Any]:
        """
        Gather information about a company's products and services.
        """
        return self.product_service_extractor.get_products_services(company_name)
    
    def get_company_leadership(self, company_name: str, domain: str = None) -> Dict[str, Any]:
        """
        Get information about a company's leadership team.
        """
        return self.leadership_extractor.get_leadership_info(company_name, domain)
    
    def get_company_news(self, company_name: str, limit: int = 5) -> Dict[str, Any]:
        """
        Get recent news about the company.
        
        Args:
            company_name (str): Name of the company
            limit (int): Maximum number of news items to return
            
        Returns:
            dict: Recent news about the company
        """
        return self.news_extractor.get_company_news(company_name, limit)
    
    def get_competitive_analysis(self, company_name: str) -> Dict[str, Any]:
        """
        Get competitive analysis for a company.
        
        Args:
            company_name (str): Name of the company
            
        Returns:
            dict: Competitive analysis data
        """
        return self.competitive_analyzer.get_competitive_analysis(company_name)
    
    def get_company_financials(self, company_name: str, domain: str = None) -> Dict[str, Any]:
        """
        Get financial information about a company.
        
        Args:
            company_name (str): Name of the company
            domain (str, optional): Company's website domain if known
            
        Returns:
            dict: Financial information about the company
        """
        return self.financials_extractor.get_financials(company_name, domain)
    
    def get_company_data(self, company_name: str) -> Dict[str, Any]:
        """
        Gather comprehensive company data.
        
        Args:
            company_name (str): Name of the company
            
        Returns:
            dict: Aggregated company data
        """
        return self.data_extractor.get_company_data(company_name)
