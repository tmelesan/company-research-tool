"""Domain validation utilities."""

import re
from typing import Tuple, List
from urllib.parse import urlparse
import tldextract

def validate_domain(domain: str) -> Tuple[bool, str]:
    """
    Validate and clean a domain name.
    
    Args:
        domain (str): Domain name to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, cleaned_domain or error_message)
    """
    if not domain:
        return False, "Domain cannot be empty"
    
    # Remove any whitespace
    domain = domain.strip()
    
    # Remove common prefixes if present
    domain = re.sub(r'^(https?://)?(www\.)?', '', domain)
    
    # Remove any trailing paths or query parameters
    domain = domain.split('/')[0]
    
    # Check domain format using tldextract to handle various TLDs correctly
    ext = tldextract.extract(domain)
    if not all([ext.domain, ext.suffix]):
        return False, "Invalid domain format. Example: example.com"
    
    # Check length constraints
    if len(domain) > 253:  # Maximum length of a domain name
        return False, "Domain name is too long"
    
    # Check for valid characters
    if not re.match(r'^[a-zA-Z0-9.-]+$', domain):
        return False, "Domain contains invalid characters"
    
    # Check each part length and format
    parts = domain.split('.')
    for part in parts:
        if len(part) > 63:  # Maximum length of each part
            return False, "Domain part is too long"
        if part.startswith('-') or part.endswith('-'):
            return False, "Domain parts cannot start or end with hyphens"
    
    # Return the cleaned domain
    return True, domain

def validate_domains(domains: List[str]) -> Tuple[List[str], List[dict]]:
    """
    Validate a list of domains and return valid domains and validation results.
    
    Args:
        domains (List[str]): List of domains to validate
        
    Returns:
        Tuple[List[str], List[dict]]: (valid_domains, validation_results)
    """
    valid_domains = []
    validation_results = []
    
    for domain in domains:
        is_valid, result = validate_domain(domain)
        validation_results.append({
            'domain': domain,
            'is_valid': is_valid,
            'result': result
        })
        if is_valid:
            valid_domains.append(result)
    
    return valid_domains, validation_results
