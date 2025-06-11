# FastAPI REST API Documentation

## Company Research Tool REST API

The Company Research Tool now includes a comprehensive REST API built with FastAPI, providing programmatic access to all research capabilities.

## 🚀 Quick Start

### Starting the API Server

```bash
# Using the launcher script (recommended)
./run_api.sh

# Or manually
source venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:

- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

## 📋 API Endpoints

### Base Endpoints

| Endpoint  | Method | Description                 |
| --------- | ------ | --------------------------- |
| `/`       | GET    | API information and version |
| `/health` | GET    | Health check endpoint       |

### Company Research Endpoints

| Endpoint                                         | Method | Description                |
| ------------------------------------------------ | ------ | -------------------------- |
| `/companies/{company_name}/exists`               | GET    | Check if company exists    |
| `/companies/{company_name}/products-services`    | GET    | Get products and services  |
| `/companies/{company_name}/leadership`           | GET    | Get leadership information |
| `/companies/{company_name}/news`                 | GET    | Get recent company news    |
| `/companies/{company_name}/competitive-analysis` | GET    | Get competitive analysis   |
| `/companies/{company_name}/financials`           | GET    | Get financial information  |
| `/companies/{company_name}/comprehensive`        | GET    | Get all company data       |

## 🔧 API Usage Examples

### 1. Check Company Existence

```bash
curl -X GET "http://localhost:8000/companies/Apple%20Inc./exists"
```

**Response:**

```json
{
  "exists": "Yes",
  "reason": "Apple Inc. is a well-known multinational technology company...",
  "industry": "Technology",
  "website_found": true,
  "website": "https://www.apple.com",
  "domain": "apple.com"
}
```

### 2. Get Products and Services

```bash
curl -X GET "http://localhost:8000/companies/Microsoft/products-services"
```

**Response:**

```json
{
  "products": ["Windows", "Office 365", "Xbox", "Azure"],
  "services": ["Cloud Computing", "Software Development", "Gaming"],
  "confidence": "High",
  "business_model": "Software and Cloud Services",
  "target_market": "Enterprise and Consumer"
}
```

### 3. Get Leadership Information

```bash
curl -X GET "http://localhost:8000/companies/Tesla/leadership?domain=tesla.com"
```

**Response:**

```json
{
  "data_available": true,
  "leadership_team": [
    {
      "name": "Elon Musk",
      "position": "CEO",
      "background": "Entrepreneur and business magnate..."
    }
  ],
  "key_executives": [...],
  "confidence": "High"
}
```

### 4. Get Recent News

```bash
curl -X GET "http://localhost:8000/companies/Google/news?limit=3"
```

**Response:**

```json
{
  "news_items": [
    {
      "title": "Google Announces New AI Features",
      "date": "2025-06-10",
      "summary": "Google introduces advanced AI capabilities...",
      "source": "TechCrunch"
    }
  ],
  "data_confidence": "High",
  "total_count": 3
}
```

### 5. Get Competitive Analysis

```bash
curl -X GET "http://localhost:8000/companies/Netflix/competitive-analysis"
```

**Response:**

```json
{
  "main_competitors": ["Disney+", "Amazon Prime", "HBO Max"],
  "market_position": "Market Leader",
  "strengths": ["Content Library", "Global Reach", "Technology"],
  "weaknesses": ["Increasing Competition", "Content Costs"],
  "competitive_advantages": ["Original Content", "Recommendation Algorithm"]
}
```

### 6. Get Financial Information

```bash
curl -X GET "http://localhost:8000/companies/Amazon/financials"
```

**Response:**

```json
{
  "data_available": true,
  "financial_information": {
    "company": "Amazon Inc.",
    "ticker": "AMZN",
    "financials": {
      "revenue": {
        "latestQuarter": {
          "value": 143313000000,
          "period": "Q4 2024",
          "currency": "USD"
        }
      },
      "profit": {...},
      "keyRatios": {...}
    }
  },
  "source": "Gemini AI"
}
```

### 7. Get Comprehensive Data

```bash
curl -X GET "http://localhost:8000/companies/IBM/comprehensive"
```

**Response:**

```json
{
  "company_name": "IBM",
  "exists": true,
  "description": "International Business Machines Corporation...",
  "industry": "Technology",
  "founding_year": 1911,
  "headquarters": "Armonk, New York",
  "data_confidence": "high",
  "data_sources": ["gemini_ai", "web_scraping"]
}
```

## 🔐 Authentication

Currently, the API uses environment variables for authentication:

```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

## 📊 Response Format

All API responses follow a consistent JSON format with appropriate HTTP status codes:

- **200 OK**: Successful request
- **400 Bad Request**: Invalid parameters
- **404 Not Found**: Company or endpoint not found
- **500 Internal Server Error**: Server error
- **503 Service Unavailable**: Service not initialized

### Error Response Format

```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## 🧪 Testing the API

### Interactive Testing

1. **Swagger UI**: Visit http://localhost:8000/docs
2. **ReDoc**: Visit http://localhost:8000/redoc

### Command Line Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test with authentication
export GEMINI_API_KEY="your-key"
curl -X GET "http://localhost:8000/companies/Apple/exists"
```

### Python Client Example

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

# Test company existence
response = requests.get(f"{BASE_URL}/companies/Apple Inc./exists")
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.status_code} - {response.text}")

# Get comprehensive data
response = requests.get(f"{BASE_URL}/companies/Microsoft/comprehensive")
company_data = response.json()
print(f"Company: {company_data.get('company_name')}")
print(f"Industry: {company_data.get('industry')}")
```

### JavaScript/Node.js Client Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

async function getCompanyInfo(companyName) {
  try {
    const response = await axios.get(
      `${BASE_URL}/companies/${encodeURIComponent(companyName)}/exists`
    );
    console.log('Company Info:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

// Usage
getCompanyInfo('Apple Inc.');
```

## 🚀 Production Deployment

### Environment Variables

```bash
# Required
export GEMINI_API_KEY="your-gemini-api-key"

# Optional
export PORT=8000
export HOST="0.0.0.0"
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Settings

For production deployment, consider:

1. **CORS Settings**: Configure `allow_origins` for specific domains
2. **Rate Limiting**: Implement rate limiting for API endpoints
3. **Authentication**: Add proper API key authentication
4. **Logging**: Configure structured logging
5. **Monitoring**: Add health checks and metrics

## 📝 API Versioning

Current API version: **2.1.1**

The API version follows the same versioning as the main application and can be retrieved from:

- Root endpoint: `GET /`
- Health endpoint: `GET /health`

## 🛠️ Development

### Adding New Endpoints

1. Add endpoint function to `api.py`
2. Define Pydantic response model
3. Add corresponding method to `CompanyResearcher`
4. Update documentation

### Response Model Validation

All responses are validated using Pydantic models, ensuring:

- Type safety
- Automatic documentation generation
- Input/output validation
- Error handling

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Uvicorn Documentation**: https://www.uvicorn.org/

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**

   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill process
   kill -9 <PID>
   ```

2. **Module Import Errors**

   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **API Key Issues**
   ```bash
   # Check if API key is set
   echo $GEMINI_API_KEY
   # Set API key
   export GEMINI_API_KEY="your-key-here"
   ```

## 📈 Performance Considerations

- **Caching**: Consider implementing response caching for frequently requested data
- **Async Operations**: The API is built with async/await for better performance
- **Connection Pooling**: FastAPI handles connection pooling automatically
- **Resource Limits**: Monitor memory usage for large company data requests
