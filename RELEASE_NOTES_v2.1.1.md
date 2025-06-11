# Release Notes - Company Research Tool v2.1.1

**Release Date**: June 11, 2025  
**Repository**: [github.com/kpapap/company-research-tool](https://github.com/kpapap/company-research-tool)

## 🔧 **Patch Release v2.1.1**

This is a patch release that includes documentation improvements and build system enhancements following the major v2.1.0 release.

### 📝 **Documentation & Build Improvements**

- **Enhanced release notes** - improved formatting and comprehensive feature documentation
- **Package setup improvements** - better metadata and distribution configuration
- **Version tracking refinements** - streamlined version management across the codebase
- **Repository structure optimization** - cleaner project organization

### 🎯 **What's Included from v2.1.0**

#### 🌐 **Streamlit Web Interface**
- Beautiful, responsive web UI with real-time progress tracking
- Interactive dashboards with charts, metrics, and visualizations
- Research history management and export capabilities
- Mobile-friendly design with secure API key input

#### 🔧 **Enhanced Data Processing**
- Robust JSON parsing with markdown code block handling
- JavaScript comment support and manual extraction fallback
- Improved financial data extraction with real data focus
- Better error handling and data quality indicators

#### 🐛 **Bug Fixes & Stability**
- CLI syntax fixes and import issue resolution
- Test suite enhancements and improved reliability
- Graceful error handling when data is unavailable

## 📊 **Core Features**

- ✅ **Company Existence Verification** - AI-powered company validation
- ✅ **Products & Services Analysis** - comprehensive offering extraction
- ✅ **Leadership Information** - executive and management team data
- ✅ **News Monitoring** - recent company news and updates
- ✅ **Competitive Analysis** - market position and competitor insights
- ✅ **Financial Data** - revenue, profit, ratios, and key metrics
- ✅ **Web Scraping** - intelligent data collection enhancement
- ✅ **Modular Architecture** - clean, maintainable, extensible codebase

## 🚀 **Quick Start**

```bash
git clone https://github.com/kpapap/company-research-tool.git
cd company-research-tool
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
./run_streamlit.sh
```

## 🎯 **Usage Modes**

1. **🌐 Web Interface** (Recommended) - `./run_streamlit.sh`
2. **💻 Command Line** - `python cli.py --company "Apple Inc." --all`
3. **📝 Python API** - `from src import CompanyResearcher`

## 📋 **Requirements**

- Python 3.7+ (tested up to 3.12)
- Google Gemini API key ([get one here](https://ai.google.dev/))
- Internet connection for API calls and web scraping

## 🔗 **Links**

- **📖 Documentation**: [README.md](https://github.com/kpapap/company-research-tool#readme)
- **🐛 Report Issues**: [GitHub Issues](https://github.com/kpapap/company-research-tool/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/kpapap/company-research-tool/discussions)

---

**Full Changelog**: [v2.1.0...v2.1.1](https://github.com/kpapap/company-research-tool/compare/v2.1.0...v2.1.1)

**Previous Release**: [v2.1.0 Release Notes](https://github.com/kpapap/company-research-tool/releases/tag/v2.1.0)

---

**Happy researching! 🔍**
