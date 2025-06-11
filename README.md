# Company Research Tool

A comprehensive Python tool for researching companies using Google's Gemini AI and web scraping technologies. This tool provides detailed information about companies including their existence, products/services, leadership, news, competitive analysis, and financial data.

## 🚀 Features

- **Company Existence Verification**: Check if a company exists and get basic industry information
- **Products & Services Analysis**: Extract detailed information about company offerings
- **Leadership Information**: Gather data about company executives and management team
- **News Monitoring**: Get recent news and updates about companies
- **Competitive Analysis**: Analyze market position, competitors, strengths, and weaknesses
- **Financial Data**: Extract financial information and key metrics
- **Comprehensive Reporting**: Aggregate all data into comprehensive company profiles
- **Web Scraping**: Enhanced data collection through intelligent web scraping
- **Modular Architecture**: Clean, maintainable, and extensible codebase
- **Enhanced JSON Parsing**: Robust JSON parsing with fallback mechanisms for malformed responses
- **Improved Financial Data**: Better prompts for real financial data extraction (no placeholders)
- **Web Interface**: Beautiful Streamlit-based web UI with interactive dashboards and visualizations

## 🆕 Recent Updates

### Version 2.1.0 (June 2025)

#### 🚀 Enhanced Financial Data Extraction

- **Improved API Prompts**: Redesigned prompts to request real financial data instead of placeholder templates
- **Structured JSON Responses**: Better-defined JSON schemas for consistent financial data format
- **Real Data Focus**: Added explicit instructions to avoid placeholder/template data in API responses
- **Support for Both Public & Private Companies**: Different extraction strategies for public vs private companies

#### 🔧 JSON Parsing Improvements

- **Markdown Code Block Handling**: Better extraction of JSON from markdown-wrapped responses (`json...`)
- **JavaScript Comment Support**: Automatic removal of JS-style comments (`//` and `/* */`) from JSON
- **Manual Extraction Fallback**: When JSON parsing fails, attempts manual key-value extraction
- **Field Mapping**: Automatic mapping between `company` and `company_name` fields for compatibility
- **Control Character Handling**: Improved handling of invalid control characters in JSON responses

#### 🐛 Bug Fixes

- **CLI Syntax Error**: Fixed indentation issues in command-line interface
- **Import Path Issues**: Resolved module import problems for CLI execution
- **Test Suite Compatibility**: Enhanced test reliability and error handling

#### 📊 Data Quality Improvements

- **Anti-Placeholder Measures**: Explicit prompting to prevent template/placeholder responses
- **Confidence Indicators**: Better data confidence and source attribution
- **Error Handling**: Improved graceful degradation when data is unavailable

#### 🌐 New Web Interface (Streamlit)

- **Interactive Dashboard**: Beautiful web-based interface with real-time progress tracking
- **Visual Data Presentation**: Charts, metrics, and formatted displays for all research types
- **Export Capabilities**: Download results as JSON or CSV directly from the browser
- **Research History**: Access and review previous research sessions
- **Mobile-Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Secure Configuration**: Safe API key input with browser-based configuration

## 📋 Requirements

- Python 3.7 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev/))
- Internet connection for web scraping and API calls

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kpapap/company-research-tool.git
cd company-research-tool
```

### 2. Set Up Python Environment

```bash
# Using pyenv (recommended)
pyenv install 3.11.12
pyenv local 3.11.12

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Application

#### Option A: Web Interface (Recommended)

```bash
# Quick launch with the provided script
./run_streamlit.sh

# Or manually
source venv/bin/activate
streamlit run streamlit_app.py
```

The web interface will automatically open in your browser at `http://localhost:8501`

#### Option B: Command Line Interface

```bash
# Basic usage example
python cli.py --company "Apple Inc." --exists
```

### 4. Configure API Key

Choose one of the following methods:

#### Option A: Environment Variable

```bash
# For macOS/Linux
export GEMINI_API_KEY="your_api_key_here"

# For Windows (Command Prompt)
set GEMINI_API_KEY=your_api_key_here

# For Windows (PowerShell)
$env:GEMINI_API_KEY = "your_api_key_here"
```

#### Option B: .env File

```bash
cp .env.example .env
# Edit .env file and add your API key
```

#### Option C: Direct Parameter

Pass the API key directly when initializing the tool (see usage examples below).

## 🎯 Usage

### Web Interface (Streamlit) - **NEW!** 🌐

The easiest way to use the tool is through the beautiful web interface:

```bash
# Quick start - launches the web app
./run_streamlit.sh

# Or manually
source venv/bin/activate
streamlit run streamlit_app.py
```

**Web Interface Features:**

- 🎨 **Beautiful UI**: Modern, responsive web interface
- 📊 **Interactive Dashboard**: Visual summaries with charts and metrics
- 🔄 **Real-time Progress**: Live progress tracking during research
- 💾 **Export Options**: Download results as JSON or CSV
- 📱 **Mobile Friendly**: Works on desktop, tablet, and mobile
- 🔐 **Secure API Key Input**: Enter your API key securely in the browser
- 📚 **Research History**: Access previous research results
- 🎛️ **Advanced Controls**: Configure all research options visually

The web interface will open automatically in your browser at `http://localhost:8501`

### Command Line Interface (CLI)

The easiest way to use the tool is through the command line interface:

```bash
# Activate virtual environment
source venv/bin/activate

# Basic usage - check if a company exists
python cli.py --company "Apple Inc." --exists
# OR
./cli.py --company "Apple Inc." --exists

# Get all information about a company
python cli.py --company "Apple Inc." --all

# Get specific information
python cli.py --company "Microsoft" --products --leadership --news

# Save results to a JSON file
python cli.py --company "Google" --comprehensive --output google_report.json

# Secure API key input (recommended)
./run_cli.sh --company "Apple Inc." --all

# Get help and see all options
python cli.py --help
```

#### Secure API Key Usage

For secure API key input, use the provided script:

```bash
# This will prompt for your API key securely (hidden input)
./run_cli.sh --company "Apple Inc." --exists

# Or set the environment variable first
export GEMINI_API_KEY="your_api_key_here"
python cli.py --company "Apple Inc." --all
```

#### CLI Options

**Research Types:**

- `--exists, -e`: Check if company exists
- `--products, -p`: Get products and services
- `--leadership, -l`: Get leadership information
- `--news, -n`: Get recent news
- `--competitive, -comp`: Get competitive analysis
- `--financials, -f`: Get financial information
- `--comprehensive, -comp-data`: Get comprehensive company data
- `--all, -a`: Run all research types

**Configuration:**

- `--api-key`: Specify Google Gemini API key
- `--no-web-scraping`: Disable web scraping (API only)
- `--news-limit`: Number of news items (default: 5)

**Output:**

- `--output, -o`: Save results to JSON file
- `--json`: Output in JSON format
- `--quiet, -q`: Suppress formatting

#### CLI Examples

```bash
# Quick company check
./cli.py -c "Tesla" -e

# Comprehensive analysis with custom API key
./cli.py --company "Amazon" --all --api-key "your-api-key"

# Financial and competitive analysis only
./cli.py -c "Netflix" -f -comp

# Get news with custom limit and save to file
./cli.py -c "Apple" -n --news-limit 10 -o apple_news.json

# JSON output for programmatic use
./cli.py -c "Microsoft" --products --json
```

### Python API Usage

You can also use the tool directly in your Python code:

### Basic Usage

```python
from src import CompanyResearcher

# Initialize the researcher
researcher = CompanyResearcher()

# Check if a company exists
result = researcher.check_company_exists("Apple Inc.")
print(result)

# Get company products and services
products = researcher.get_company_products_services("Apple Inc.")
print(products)

# Get leadership information
leadership = researcher.get_company_leadership("Apple Inc.")
print(leadership)

# Get recent news
news = researcher.get_company_news("Apple Inc.", limit=5)
print(news)

# Get competitive analysis
competition = researcher.get_competitive_analysis("Apple Inc.")
print(competition)

# Get financial information
financials = researcher.get_company_financials("Apple Inc.")
print(financials)

# Get comprehensive company data
comprehensive_data = researcher.get_company_data("Apple Inc.")
print(comprehensive_data)
```

### Advanced Usage

```python
# Initialize with custom API key and disable web scraping
researcher = CompanyResearcher(
    api_key="your_api_key_here",
    use_web_scraping=False
)

# Research multiple companies
companies = ["Apple Inc.", "Microsoft Corporation", "Google LLC"]
results = {}

for company in companies:
    results[company] = researcher.get_company_data(company)

# Print results
for company, data in results.items():
    print(f"\n--- {company} ---")
    print(f"Industry: {data.get('industry', 'Unknown')}")
    print(f"Description: {data.get('description', 'N/A')}")
```

## 🏗️ Architecture

The tool follows a modular architecture for maintainability and extensibility:

```
src/
├── company_researcher.py          # Main orchestrator class
├── data_extractors/               # Specialized data extractors
│   ├── company_existence.py       # Company existence verification
│   ├── products_services.py       # Products & services extraction
│   ├── leadership.py              # Leadership information
│   ├── company_news.py            # News gathering
│   ├── competitive_analysis.py    # Competitive analysis
│   ├── financials.py              # Financial data extraction
│   └── company_data.py            # Comprehensive data aggregation
├── services/                      # Core services
│   ├── gemini_service.py          # Google Gemini API wrapper
│   └── web_scraper.py             # Web scraping functionality
└── utils/                         # Utility functions
    ├── json_helper.py             # JSON parsing utilities
    └── logger.py                  # Logging configuration

# User Interfaces
cli.py                             # Command-line interface
streamlit_app.py                   # Web-based interface (Streamlit)
run_streamlit.sh                   # Web app launcher script
```

### Key Components

#### CompanyResearcher

The main class that orchestrates all research operations. It initializes and coordinates various data extractors and services.

#### Data Extractors

Specialized classes for different types of company information:

- `CompanyExistenceChecker`: Verifies company existence and basic info
- `ProductServiceExtractor`: Extracts products and services information
- `LeadershipExtractor`: Gathers leadership and management data
- `CompanyNewsExtractor`: Collects recent news and updates
- `CompetitiveAnalysisExtractor`: Performs competitive analysis
- `CompanyFinancialsExtractor`: Extracts financial information
- `CompanyDataExtractor`: Aggregates comprehensive company data

#### Services

Core services that handle external integrations:

- `GeminiService`: Manages Google Gemini API interactions
- `WebScraper`: Handles web scraping operations

#### Utilities

Helper functions for common operations:

- `json_helper`: JSON parsing and extraction utilities
- `logger`: Centralized logging configuration

## 🧪 Testing

The project includes a comprehensive test suite covering all major functionality.

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_company_researcher.py::TestCompanyResearcher::test_company_existence -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Secure Testing with API Key

Use the provided script for secure API key input:

```bash
./run_tests.sh
```

This script will prompt you to enter your API key securely (hidden input) and then run the full test suite.

### Test Coverage

The test suite includes:

- Company existence verification tests
- Products and services extraction tests
- Leadership information tests
- News gathering tests
- Competitive analysis tests
- Financial data extraction tests
- Comprehensive data aggregation tests
- Error handling and edge case tests
- Invalid input validation tests

## 📊 API Response Formats

### Company Existence

```json
{
  "exists": "Yes",
  "industry": "Technology",
  "reason": "Apple Inc. is a well-known technology company..."
}
```

### Products & Services

```json
{
  "products": ["iPhone", "iPad", "Mac", "Apple Watch"],
  "services": ["iCloud", "Apple Music", "App Store"],
  "confidence": "High"
}
```

### Leadership

```json
{
  "data_available": true,
  "leadership_team": [
    {
      "name": "Tim Cook",
      "position": "CEO",
      "background": "..."
    }
  ]
}
```

### News

```json
{
  "news_items": [
    {
      "title": "Apple Announces New Product",
      "date": "2024-01-15",
      "summary": "...",
      "source": "..."
    }
  ],
  "data_confidence": "High"
}
```

### Competitive Analysis

```json
{
  "main_competitors": ["Microsoft", "Google", "Samsung"],
  "market_position": "Market Leader",
  "strengths": ["Strong brand", "Innovation"],
  "weaknesses": ["High prices"]
}
```

### Financial Information

#### Public Companies (New Enhanced Format)

```json
{
  "data_available": true,
  "financial_information": {
    "company": "Apple Inc.",
    "ticker": "AAPL",
    "lastUpdated": "2024-Q4",
    "financials": {
      "revenue": {
        "latestQuarter": {
          "value": 91816000000,
          "period": "Q4 2024",
          "currency": "USD"
        }
      },
      "profit": {
        "latestQuarter": {
          "value": 20553000000,
          "period": "Q4 2024",
          "currency": "USD"
        }
      },
      "keyRatios": {
        "peRatio": { "value": 28.5, "asOfDate": "2024-12-31" },
        "eps": { "value": 6.43, "asOfDate": "2024-12-31" }
      }
    },
    "recentNews": [
      {
        "headline": "Apple Reports Record Q4 Earnings",
        "source": "Reuters",
        "date": "2024-01-15"
      }
    ]
  },
  "source": "Gemini AI"
}
```

#### Private Companies

```json
{
  "data_available": true,
  "financial_information": {
    "company": "Private Corp Inc.",
    "companyType": "private",
    "financials": {
      "estimatedRevenue": {"value": 500000000, "year": "2024", "source": "industry_reports"},
      "funding": {
        "totalFunding": 100000000,
        "lastRound": {"amount": 50000000, "date": "2024-03-15", "type": "Series B"}
      },
      "employees": 1200
    },
    "recentNews": [...]
  },
  "source": "Gemini AI"
}
```

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Optional Parameters

- `use_web_scraping`: Enable/disable web scraping (default: True)
- `timeout`: HTTP request timeout in seconds (default: 10)
- `user_agent`: Custom User-Agent for web requests

## 📝 Logging

The tool includes comprehensive logging for debugging and monitoring:

```python
import logging

# Set logging level
logging.getLogger('src').setLevel(logging.DEBUG)

# Logs are automatically configured and will show:
# - API requests and responses
# - Web scraping operations
# - Data extraction progress
# - Error messages and stack traces
```

## 🚨 Error Handling

The tool includes robust error handling:

- **API Errors**: Graceful handling of API rate limits, invalid keys, and network issues
- **Web Scraping Errors**: Timeout handling, invalid URLs, and blocked requests
- **Data Parsing Errors**: JSON parsing failures and malformed responses
- **Input Validation**: Empty inputs, invalid company names, and parameter validation

## 🔒 Privacy and Ethics

- **Rate Limiting**: Respects API rate limits and implements delays
- **User-Agent**: Uses identifiable User-Agent headers for web scraping
- **Data Usage**: Only extracts publicly available information
- **API Compliance**: Follows Google Gemini API terms of service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation for new features
- Ensure all tests pass before submitting

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI**: For providing the powerful AI capabilities
- **Beautiful Soup**: For HTML parsing and web scraping
- **Trafilatura**: For advanced text extraction
- **Requests**: For HTTP operations

## 🐛 Troubleshooting

### Common Issues

1. **API Key Issues**

   ```
   Error: No Gemini API key provided
   Solution: Set GEMINI_API_KEY environment variable or pass api_key parameter
   ```

2. **Import Errors**

   ```
   Error: ModuleNotFoundError: No module named 'src'
   Solution: Ensure you're running from the project root directory
   ```

3. **Web Scraping Blocked**

   ```
   Error: 403 Forbidden or timeout errors
   Solution: Some websites block automated requests; this is expected behavior
   ```

4. **JSON Parsing Issues**

   ````
   Error: Failed to parse JSON response
   Solution: The tool now includes automatic fallback mechanisms:
   - Handles markdown code blocks (```json...```)
   - Removes JavaScript-style comments
   - Attempts manual extraction for malformed JSON
   - Check logs for detailed parsing information
   ````

5. **Placeholder Data in Financial Results**

   ```
   Issue: Getting template/placeholder data instead of real financial figures
   Solution: Updated prompts now explicitly request real data only
   - Verify your API key has access to current data
   - Some companies may have limited publicly available financial data
   - Private companies will have less detailed financial information
   - Look for source attribution to understand data origin
   ```

   **Expected vs Problematic Output:**

   ```
   ❌ Problematic: "Placeholder - Replace with actual news headline"
   ✅ Expected: "Apple Reports Record Q4 Revenue of $91.8B"

   ❌ Problematic: {'value': None, 'period': 'TTM'}
   ✅ Expected: {'value': 28.5, 'period': 'Q4 2024'}
   ```

6. **Rate Limit Exceeded**

   ```
   Error: 429 Too Many Requests
   Solution: Implement delays between requests or use a different API key tier
   ```

7. **Streamlit Download Buttons Disappearing**
   ```
   Issue: Download buttons disappear after clicking in the web interface
   Solution: This issue has been fixed with persistent session state
   - Download buttons now remain available after clicking
   - Use the "Clear Downloads" button to hide them when done
   - Switch between previous research results using the dropdown
   ```

### Getting Help

If you encounter issues:

1. Check the [Issues](../../issues) page for similar problems
2. Enable debug logging to get more detailed error information
3. Verify your API key is valid and has sufficient quota
4. Ensure all dependencies are properly installed

## 📊 Data Quality & Expectations

### Financial Data Quality

The tool has been enhanced to provide real financial data rather than placeholder templates:

#### ✅ What to Expect

- **Real Numbers**: Actual revenue, profit, and ratio figures for public companies
- **Current Data**: Recent quarterly/annual financial information
- **Source Attribution**: Clear indication of data sources (Gemini AI, web scraping, etc.)
- **Structured Format**: Consistent JSON structure with proper data types

#### ⚠️ Limitations

- **Private Companies**: Limited financial data availability for non-public companies
- **Data Freshness**: AI model training data may not include the most recent financial reports
- **Market Hours**: Real-time stock data is not provided
- **Availability**: Some companies may have limited publicly available financial information

#### 🔍 Data Validation

- Results include confidence indicators and source attribution
- Manual extraction fallback ensures some data is always returned
- Null values indicate genuinely unavailable data (not parsing errors)

### Response Quality Indicators

Look for these indicators of data quality:

- `source`: Indicates where the data came from (Gemini AI, website, manual extraction)
- `_manual_extraction`: Present when JSON parsing failed but data was extracted manually
- `data_available`: Boolean indicating if meaningful data was found
- `confidence` or `data_confidence`: Quality assessment when available

## 📈 Performance Tips

- **Batch Processing**: Process multiple companies in batches rather than individually
- **Caching**: Implement caching for frequently requested companies
- **Parallel Processing**: Use threading for independent company research
- **API Optimization**: Use appropriate timeouts and retry strategies

---

**Happy researching! 🔍**
