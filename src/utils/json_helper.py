import json
import re

def extract_json_from_response(text: str):
    """
    Extract JSON from Gemini response text.
    
    Args:
        text (str): Response text from Gemini API
        
    Returns:
        dict: Extracted JSON data
    """
    try:
        # Find JSON content between code blocks if present
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            json_str = text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            json_str = text[start:end].strip()
        else:
            # Try to parse the whole text as JSON
            json_str = text.strip()
        
        # Remove JavaScript-style comments that break JSON parsing
        # Remove single-line comments (// comment)
        json_str = re.sub(r'//.*?(?=\n|$)', '', json_str)
        
        # Remove multi-line comments (/* comment */)
        json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
        
        # Clean up any trailing commas that might be left after comment removal
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        
        # Try to parse the cleaned JSON first before handling control characters
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Only if initial parsing fails, try to handle control characters
            # Handle invalid control characters that break JSON parsing
            # But be careful not to replace characters inside valid JSON strings
            
            # First, let's try a more conservative approach
            # Replace control characters that are clearly outside of strings
            lines = json_str.split('\n')
            cleaned_lines = []
            
            for line in lines:
                # Remove or escape other invalid control characters (ASCII 0-31)
                # but preserve newlines that are part of the structure
                line = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', line)
                cleaned_lines.append(line)
            
            json_str = '\n'.join(cleaned_lines)
            
            # Try parsing again
            return json.loads(json_str)
        
    except json.JSONDecodeError as e:
        # If parsing still fails, try to extract key information manually
        try:
            # Attempt a more lenient approach for common patterns
            return _attempt_manual_json_extraction(text)
        except:
            # If all else fails, return the raw text with detailed error info
            return {
                "error": "Failed to parse JSON response",
                "raw_text": text[:1000] + "..." if len(text) > 1000 else text,
                "parse_error": str(e),
                "error_position": f"line {e.lineno} column {e.colno}" if hasattr(e, 'lineno') else "unknown"
            }
    except Exception as e:
        return {
            "error": f"Unexpected error during JSON parsing: {str(e)}",
            "raw_text": text[:500] + "..." if len(text) > 500 else text
        }


def _attempt_manual_json_extraction(text: str):
    """
    Attempt to manually extract key-value pairs when JSON parsing fails.
    This is a fallback for malformed JSON.
    """
    result = {}
    
    # Look for common patterns in API responses
    patterns = {
        'company': r'"company":\s*"([^"]*)"',
        'company_name': r'"company_name":\s*"([^"]*)"',
        'ticker': r'"ticker":\s*"([^"]*)"',
        'exists': r'"exists":\s*"([^"]*)"',
        'industry': r'"industry":\s*"([^"]*)"',
        'description': r'"description":\s*"([^"]*)"',
        'reason': r'"reason":\s*"([^"]*)"'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result[key] = match.group(1)
    
    # If we found 'company' but not 'company_name', map them
    if 'company' in result and 'company_name' not in result:
        result['company_name'] = result['company']
    
    # If we found 'company_name' but not 'company', map them
    if 'company_name' in result and 'company' not in result:
        result['company'] = result['company_name']
    
    if result:
        result['_manual_extraction'] = True
        return result
    else:
        raise ValueError("Could not extract any meaningful data")
