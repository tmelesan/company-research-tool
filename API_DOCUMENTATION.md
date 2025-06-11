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

**⚠️ Note:** The API returns the exact same detailed, structured data as the CLI tool. These are real response formats from the Company Research Tool.

### 1. Check Company Existence

```bash
curl -X GET "http://localhost:8000/companies/Apple%20Inc./exists"
```

**Response:**

```json
{
  "exists": "Yes",
  "reason": "Apple Inc. is a well-known, publicly traded multinational technology company based in Cupertino, California.",
  "industry": "Technology, Consumer Electronics, Software",
  "website_found": true,
  "website": "https://www.apple.com",
  "domain": "apple.com"
}
```

### 2. Get Products and Services

```bash
curl -X GET "http://localhost:8000/companies/Amazon/products-services"
```

**Response:**

```json
{
  "products": [
    "Electronics (Kindle, Fire tablets, Echo devices)",
    "Books (physical and digital)",
    "Apparel and Accessories",
    "Home and Kitchen goods",
    "Beauty and Personal Care products",
    "Grocery (Amazon Fresh, Whole Foods Market)",
    "Amazon Basics (private label products)"
  ],
  "services": [
    "E-commerce (online retail)",
    "Cloud Computing (Amazon Web Services - AWS)",
    "Digital Streaming (Amazon Prime Video, Amazon Music)",
    "Digital Advertising",
    "Logistics and Fulfillment (Fulfillment by Amazon - FBA)",
    "Artificial Intelligence (AI) and Machine Learning (ML) services"
  ],
  "confidence": "High"
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
  "company_name": "Tesla",
  "leadership_team": [
    {
      "name": "Elon Musk",
      "position": "CEO and Product Architect",
      "background": "Entrepreneur and business magnate known for leading multiple companies including SpaceX and Tesla"
    },
    {
      "name": "Zachary Kirkhorn",
      "position": "CFO",
      "background": "Former Senior Vice President of Finance at Tesla with extensive automotive industry experience"
    },
    {
      "name": "Drew Baglino",
      "position": "Senior Vice President, Powertrain and Energy Engineering",
      "background": "Long-time Tesla executive responsible for vehicle engineering and energy products"
    }
  ],
  "source": "AI generated"
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
      "title": "Google Announces Major AI Breakthrough in Quantum Computing",
      "date": "2025-06-01",
      "summary": "Google researchers have achieved a significant milestone in quantum computing with their latest AI-powered quantum processor, demonstrating quantum supremacy in solving complex mathematical problems.",
      "source": "TechCrunch"
    },
    {
      "title": "Alphabet Reports Strong Q1 2025 Earnings Driven by Cloud Growth",
      "date": "2025-05-28",
      "summary": "Google parent company Alphabet exceeded analyst expectations with robust revenue growth in its cloud computing division and continued strength in advertising revenue.",
      "source": "Reuters"
    },
    {
      "title": "Google Launches Enhanced Gemini AI Assistant Features",
      "date": "2025-05-15",
      "summary": "Google unveiled new capabilities for its Gemini AI assistant, including improved multimodal understanding and integration with Google Workspace applications.",
      "source": "The Verge"
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
  "main_competitors": [
    "Disney+ (The Walt Disney Company)",
    "Amazon Prime Video (Amazon)",
    "HBO Max (Warner Bros. Discovery)",
    "Hulu (Disney)",
    "Apple TV+ (Apple)",
    "Paramount+ (Paramount Global)",
    "Peacock (NBCUniversal)"
  ],
  "market_position": "Market Leader in Global Streaming",
  "strengths": [
    "Extensive global content library",
    "Strong original content production",
    "Advanced recommendation algorithm",
    "Global market presence in 190+ countries",
    "User-friendly interface and experience",
    "Multiple pricing tiers and plans"
  ],
  "weaknesses": [
    "Increasing content costs and competition for rights",
    "Limited live sports content compared to competitors",
    "Rising subscription costs may impact customer retention",
    "Dependence on third-party content providers",
    "Currency fluctuation impacts in international markets"
  ],
  "competitive_advantages": [
    "First-mover advantage in streaming",
    "Proprietary recommendation technology",
    "Significant investment in original content",
    "Global distribution network"
  ]
}
```

### 6. Get Financial Information

```bash
curl -X GET "http://localhost:8000/companies/Apple/financials"
```

**Response:**

```json
{
  "data_available": true,
  "financial_information": {
    "company": "Apple Inc.",
    "ticker": "AAPL",
    "lastUpdated": "Q1 2025",
    "financials": {
      "revenue": {
        "latestQuarter": {
          "value": 119575000000,
          "period": "Q1 2025",
          "currency": "USD"
        }
      },
      "profit": {
        "latestQuarter": {
          "value": 33916000000,
          "period": "Q1 2025",
          "currency": "USD"
        }
      },
      "keyRatios": {
        "peRatio": {
          "value": 29.2,
          "asOfDate": "2025-06-01"
        },
        "eps": {
          "value": 2.18,
          "asOfDate": "2025-06-01"
        }
      }
    },
    "recentNews": [
      {
        "headline": "Apple Reports Record Q1 Revenue of $119.6B",
        "source": "Apple Inc.",
        "date": "2025-02-01"
      },
      {
        "headline": "iPhone 16 Sales Drive Strong Quarter for Apple",
        "source": "Reuters",
        "date": "2025-02-02"
      }
    ]
  },
  "source": "Gemini AI"
}
```

### 7. Get Comprehensive Data (Equivalent to CLI `--all` flag)

```bash
curl -X GET "http://localhost:8000/companies/Tesla/comprehensive"
```

**Response:**

```json
{
  "company_name": "Tesla, Inc.",
  "exists": true,
  "description": "Tesla, Inc. is an American multinational automotive and clean energy company headquartered in Austin, Texas. Tesla designs and manufactures electric vehicles, battery energy storage systems, and related products and services.",
  "industry": "Automotive, Clean Energy, Technology",
  "founding_year": 2003,
  "headquarters": "Austin, Texas, United States",
  "products_services": [
    "Model S (luxury sedan)",
    "Model 3 (compact executive sedan)",
    "Model X (mid-size SUV)",
    "Model Y (compact SUV)",
    "Cybertruck (pickup truck)",
    "Tesla Semi (electric truck)",
    "Tesla Roadster (sports car)",
    "Powerwall (home battery)",
    "Powerpack (commercial battery)",
    "Megapack (utility-scale battery)",
    "Solar panels and solar roof tiles",
    "Supercharger network",
    "Full Self-Driving (FSD) software"
  ],
  "key_people": [
    "Elon Musk (CEO and Product Architect)",
    "Zachary Kirkhorn (CFO)",
    "Drew Baglino (SVP, Powertrain and Energy Engineering)",
    "Lars Moravy (VP of Vehicle Engineering)"
  ],
  "competitors": [
    "Ford (F-150 Lightning, Mustang Mach-E)",
    "General Motors (Chevrolet Bolt, Cadillac Lyriq)",
    "Volkswagen (ID series)",
    "BMW (iX, i4)",
    "Mercedes-EQS",
    "Rivian (R1T, R1S)",
    "Lucid Motors (Air)",
    "NIO",
    "BYD"
  ],
  "website": "https://www.tesla.com",
  "social_media": {
    "twitter": "@Tesla",
    "instagram": "@teslamotors",
    "youtube": "@Tesla"
  },
  "public_company": true,
  "stock_symbol": "TSLA",
  "estimated_size": "140,000+ employees",
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

Current API version: **2.2.0**

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
