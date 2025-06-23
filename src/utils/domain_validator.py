"""Domain validation utilities."""

from typing import Tuple, List
import socket
import requests
import tldextract
from urllib.parse import urlparse
from ..utils.logger import setup_logger

logger = setup_logger()

# Common TLDs that shouldn't be considered part of company names
COMMON_TLDS = {
    'com', 'net', 'org', 'edu', 'gov', 'mil', 'int', 'eu', 'uk', 
    'us', 'ca', 'au', 'de', 'fr', 'jp', 'ru', 'cn', 'in', 'br'
}

# Common words that might appear in company names but should be ignored in matching
COMMON_BUSINESS_WORDS = {
    'inc', 'corp', 'corporation', 'llc', 'ltd', 'limited', 'company',
    'co', 'group', 'holdings', 'international', 'global', 'worldwide',
    'solutions', 'services', 'technologies', 'systems', 'software'
}

def _clean_company_name(name: str) -> str:
    """Helper function to clean company names for comparison."""
    name = name.lower().strip()
    
    # Remove common business suffixes
    for suffix in COMMON_BUSINESS_WORDS:
        if name.endswith(f" {suffix}"):
            name = name[:-len(suffix)].strip()
            
    return name

def validate_domain(domain: str) -> Tuple[bool, str]:
    """
    Validate if a domain is properly formatted and exists.
    
    Args:
        domain (str): The domain to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    try:
        # Basic format validation
        if not domain or not '.' in domain:
            return False, "Invalid domain format"
            
        # Clean up domain
        domain = domain.strip().lower()
        if domain.startswith(('http://', 'https://')):
            parsed = urlparse(domain)
            domain = parsed.netloc        # Extract and validate domain parts
        ext = tldextract.extract(domain)
        
        # Validate domain parts
        if not ext.domain:
            return False, "Invalid domain: missing domain name"
        if not ext.suffix:
            return False, "Invalid domain: unknown or invalid TLD"
            
        # Log extracted parts for debugging
        logger.info(f"Domain parts - domain: {ext.domain}, TLD: {ext.suffix}, subdomain: {ext.subdomain}")
            
        # Construct the full domain, including subdomain if present
        domain_parts = [part for part in [ext.subdomain, ext.domain, ext.suffix] if part]
        full_domain = '.'.join(domain_parts)
        
        # Store the main domain for logging
        main_domain = '.'.join([ext.domain, ext.suffix])
        logger.info(f"Validating domain: {full_domain} (main domain: {main_domain})")
        
        # DNS resolution check
        try:
            socket.gethostbyname(full_domain)
        except socket.gaierror:
            return False, "Domain does not exist (DNS lookup failed)"
              # HTTP(S) accessibility check with SSL verification handling
        https_failed = False
        ssl_error = False

        # Try HTTPS first with SSL verification
        try:
            response = requests.head(f"https://{full_domain}", timeout=5, allow_redirects=True)
            logger.info(f"HTTPS (verified) status code: {response.status_code}")
            if response.status_code < 400:
                return True, "Domain exists and is HTTPS-enabled (verified SSL)"
        except requests.exceptions.SSLError:
            ssl_error = True
            logger.warning(f"SSL verification failed for {full_domain}, trying without verification")
            # Try HTTPS without SSL verification
            try:
                response = requests.head(f"https://{full_domain}", timeout=5, allow_redirects=True, verify=False)
                logger.info(f"HTTPS (unverified) status code: {response.status_code}")
                if response.status_code < 400:
                    return True, "Domain exists and is HTTPS-enabled (unverified SSL)"
            except requests.RequestException:
                https_failed = True
        except requests.RequestException:
            https_failed = True

        # If HTTPS failed, try HTTP
        if https_failed or ssl_error:
            try:
                response = requests.head(f"http://{full_domain}", timeout=5, allow_redirects=True)
                logger.info(f"HTTP status code: {response.status_code}")
                if response.status_code < 400:
                    return True, "Domain exists (HTTP only)"
            except requests.RequestException as e:
                logger.error(f"Domain validation error: {str(e)}")
                # If we had an SSL error but HTTP also fails, domain might still exist
                if ssl_error:
                    return True, "Domain exists (SSL verification failed, HTTP unavailable)"
                return False, "Domain exists but appears to be inactive"
        
        return True, "Domain exists"
        
    except Exception as e:
        logger.error(f"Domain validation error: {str(e)}")
        return False, f"Validation error: {str(e)}"

def validate_domain_relevance(domain: str, company_name: str) -> Tuple[bool, str]:
    """
    Check if a domain appears to be related to a company name.
    
    Args:
        domain (str): The domain to check
        company_name (str): The company name to compare against
        
    Returns:
        Tuple[bool, str]: (is_relevant, message)
    """
    try:
        # Clean inputs
        domain = domain.lower().strip()
        company_name = company_name.lower().strip()
        
        # Extract domain parts
        ext = tldextract.extract(domain)
        if not ext.domain:
            return False, "Invalid domain format"
            
        # Get all relevant parts of the domain
        domain_parts = []
        if ext.subdomain:
            domain_parts.extend(ext.subdomain.split('.'))
        domain_parts.append(ext.domain)
        
        # Log the analysis
        logger.info(f"Analyzing domain relevance: {domain} for company: {company_name}")
        logger.info(f"Domain parts to check: {domain_parts}")
            
        # Remove common business suffixes from company name
        suffixes = [' inc', ' corp', ' corporation', ' llc', ' ltd', ' limited', 
                   ' company', ' co', ' group', ' holdings', ' international']
        clean_company = company_name
        for suffix in suffixes:
            if clean_company.endswith(suffix):
                clean_company = clean_company[:-len(suffix)].strip()            
        # Remove common words and normalize company name
        common_words = {'the', 'and', 'of', 'for', 'in', 'at', 'by', 'to', 'a', 'an'}
        company_words = [w for w in clean_company.split() if w not in common_words]
        
        # Normalize company name and domain parts for comparison
        company_normalized = ''.join(e for e in clean_company if e.isalnum()).lower()
        
        # Check each domain part for matches
        for domain_part in domain_parts:
            domain_normalized = ''.join(e for e in domain_part if e.isalnum()).lower()
            
            # Exact match
            if company_normalized == domain_normalized:
                return True, f"Domain part '{domain_part}' exactly matches company name"
            
            # Full company name contained in domain
            if company_normalized in domain_normalized:
                return True, f"Domain part '{domain_part}' contains full company name"
            
            # Check individual words
            main_words = [w for w in company_words if len(w) > 2]
            if main_words:
                matches = []
                for word in main_words:
                    word_normalized = ''.join(e for e in word if e.isalnum()).lower()
                    if word_normalized in domain_normalized:
                        matches.append(word)
                
                if matches:
                    return True, f"Domain contains company name parts: {', '.join(matches)}"
                
                # Check for abbreviation
                if len(main_words) > 1:
                    abbrev = ''.join(word[0] for word in main_words)
                    if abbrev.lower() == domain_normalized:
                        return True, f"Domain '{domain_part}' matches company abbreviation ({abbrev})"
                    
        return False, "Domain doesn't appear to be related to the company"
        
    except Exception as e:
        logger.error(f"Domain relevance check error: {str(e)}")
        return False, f"Relevance check error: {str(e)}"
