import unittest
from src import CompanyResearcher

class TestCompanyResearcher(unittest.TestCase):
    def setUp(self):
        # API key should be set in environment variable GEMINI_API_KEY
        self.researcher = CompanyResearcher()  # Will use env var automatically
        self.test_company = "Apple Inc."

    def test_company_existence(self):
        """Test checking if a company exists"""
        result = self.researcher.check_company_exists(self.test_company)
        self.assertIsNotNone(result)
        self.assertIn("exists", result)
        self.assertIn("industry", result)

    def test_products_services(self):
        """Test getting company products and services"""
        result = self.researcher.get_company_products_services(self.test_company)
        self.assertIsNotNone(result)
        self.assertIn("products", result)
        self.assertIn("services", result)
        self.assertIn("confidence", result)

    def test_leadership(self):
        """Test getting company leadership information"""
        result = self.researcher.get_company_leadership(self.test_company)
        self.assertIsNotNone(result)
        self.assertIn("data_available", result)
        if result.get("data_available"):
            self.assertIn("leadership_team", result)

    def test_company_news(self):
        """Test getting company news"""
        result = self.researcher.get_company_news(self.test_company)
        self.assertIsNotNone(result)
        self.assertIn("news_items", result)
        self.assertIn("data_confidence", result)

    def test_competitive_analysis(self):
        """Test getting competitive analysis"""
        result = self.researcher.get_competitive_analysis(self.test_company)
        self.assertIsNotNone(result)
        self.assertIn("main_competitors", result)
        self.assertIn("market_position", result)
        self.assertIn("strengths", result)
        self.assertIn("weaknesses", result)

    def test_financials(self):
        """Test getting financial information"""
        result = self.researcher.get_company_financials(self.test_company)
        self.assertIsNotNone(result)
        self.assertIn("data_available", result)
        self.assertIn("financial_information", result)

    def test_comprehensive_data(self):
        """Test getting comprehensive company data"""
        result = self.researcher.get_company_data(self.test_company)
        self.assertIsNotNone(result)
        self.assertIn("company_name", result)
        self.assertIn("description", result)
        self.assertIn("industry", result)
        self.assertIn("data_sources", result)

    def test_invalid_company(self):
        """Test behavior with invalid company name"""
        invalid_company = "ThisCompanyDefinitelyDoesNotExist12345"
        result = self.researcher.check_company_exists(invalid_company)
        self.assertIsNotNone(result)
        self.assertIn("exists", result)
        
    def test_error_handling(self):
        """Test error handling with empty input"""
        empty_company = ""
        result = self.researcher.check_company_exists(empty_company)
        self.assertIsNotNone(result)
        # The API handles empty input gracefully with exists='No' and reason
        self.assertIn("exists", result)
        self.assertEqual(result["exists"], "No")
        self.assertIn("reason", result)

if __name__ == '__main__':
    unittest.main()
