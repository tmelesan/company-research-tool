import unittest
from unittest.mock import Mock, patch
from src.data_extractors.company_existence import CompanyExistenceChecker
from src.services.gemini_service import GeminiService

class TestCompanyExistenceChecker(unittest.TestCase):
    def setUp(self):
        self.mock_gemini = Mock(spec=GeminiService)
        self.checker = CompanyExistenceChecker(gemini_service=self.mock_gemini)
        
        # Default mock response from Gemini
        self.mock_gemini.generate_response.return_value = {
            "exists": "Yes",
            "reason": "Company exists and is well-established",
            "industry": "Technology"
        }

    def test_check_company_exists_with_valid_domain(self):
        """Test company existence check with a valid domain"""
        # Test data
        company_name = "Example Corp"
        test_domain = "example.com"
        
        # Execute check
        result = self.checker.check_company_exists(company_name, test_domain)
        
        # Verify result structure
        self.assertIsInstance(result, dict)
        self.assertIn('company_name', result)
        self.assertIn('domains', result)
        self.assertIn('domain_validation', result)
        self.assertIn('gemini_response', result)
        self.assertIn('exists', result)
        self.assertIn('confidence', result)
        
        # Check domain validation
        self.assertIn(test_domain, result['domains'])
        
        # Verify Gemini was called with correct prompt
        prompt_call = self.mock_gemini.generate_response.call_args[0][0]
        self.assertIn(company_name, prompt_call)
        self.assertIn(test_domain, prompt_call)

    def test_check_company_exists_without_domain(self):
        """Test company existence check without providing a domain"""
        company_name = "Example Corp"
        
        result = self.checker.check_company_exists(company_name)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['domain_validation']['valid_domains'], [])
        self.assertIsNone(result['domain_validation']['exists'])
        
        # Verify Gemini was still called
        self.mock_gemini.generate_response.assert_called_once()

    def test_check_company_exists_with_invalid_domain(self):
        """Test company existence check with an invalid domain"""
        company_name = "Example Corp"
        invalid_domain = "not-a-real-domain"
        
        result = self.checker.check_company_exists(company_name, invalid_domain)
        
        self.assertIsInstance(result, dict)
        self.assertIn(invalid_domain, result['domains'])
        self.assertEqual(result['domain_validation']['valid_domains'], [])

    def test_check_company_exists_with_multiple_domains(self):
        """Test company existence check with multiple domains"""
        company_name = "Example Corp"
        domains = ["example.com", "example.org", "not-valid.xyz"]
        
        result = self.checker.check_company_exists(company_name, domains)
        
        self.assertIsInstance(result, dict)
        for domain in domains:
            self.assertIn(domain, result['domains'])
        
        # Verify only valid domains are in valid_domains list
        valid_domains = result['domain_validation']['valid_domains']
        self.assertIn("example.com", valid_domains)
        self.assertIn("example.org", valid_domains)
        self.assertNotIn("not-valid.xyz", valid_domains)

    def test_gemini_error_handling(self):
        """Test handling of Gemini API errors"""
        # Setup Gemini to return an error
        self.mock_gemini.generate_response.side_effect = Exception("API Error")
        
        result = self.checker.check_company_exists("Example Corp")
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['gemini_response']['exists'], "Error")
        self.assertIn("API Error", result['gemini_response']['reason'])

    def test_confidence_levels(self):
        """Test different confidence level calculations"""
        company_name = "Example Corp"
        valid_domain = "example.com"
        
        # Test high confidence (both domain and Gemini positive)
        result = self.checker.check_company_exists(company_name, valid_domain)
        self.assertEqual(result['confidence'], 'high')
        
        # Test medium confidence (only domain valid)
        self.mock_gemini.generate_response.return_value = {
            "exists": "No",
            "reason": "Could not verify company",
            "industry": None
        }
        result = self.checker.check_company_exists(company_name, valid_domain)
        self.assertEqual(result['confidence'], 'medium')
        
        # Test low confidence (no domain, unclear Gemini response)
        self.mock_gemini.generate_response.return_value = {
            "exists": "Unclear",
            "reason": "Insufficient information",
            "industry": None
        }
        result = self.checker.check_company_exists(company_name)
        self.assertEqual(result['confidence'], 'low')

if __name__ == '__main__':
    unittest.main()
