#!/usr/bin/env python
"""
Company Research Tool - Command Line Interface

A command-line interface for researching companies using Google's Gemini AI and web scraping.
"""

import argparse
import json
import sys
import os
from typing import Dict, Any, Optional

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from src.company_researcher import CompanyResearcher


def print_json_pretty(data: Dict[str, Any]) -> None:
    """Print JSON data in a formatted way."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def print_section_header(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f" {title.upper()}")
    print('=' * 60)


def format_company_summary(data: Dict[str, Any]) -> None:
    """Format and print a company summary."""
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
        return
    
    print(f"📊 Company: {data.get('company_name', 'Unknown')}")
    print(f"🏭 Industry: {data.get('industry', 'Unknown')}")
    print(f"📝 Description: {data.get('description', 'N/A')}")
    
    if 'data_sources' in data:
        print(f"📡 Data Sources: {', '.join(data['data_sources'])}")


def format_existence_check(data: Dict[str, Any]) -> None:
    """Format and print company existence check results."""
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
        return
    
    exists = data.get('exists', 'Unknown')
    if exists == 'Yes':
        print("✅ Company exists")
    elif exists == 'No':
        print("❌ Company does not exist")
    else:
        print(f"❓ Status: {exists}")
    
    if 'industry' in data:
        print(f"🏭 Industry: {data['industry']}")
    
    if 'reason' in data:
        print(f"💭 Details: {data['reason']}")


def format_products_services(data: Dict[str, Any]) -> None:
    """Format and print products and services information."""
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
        return
    
    if 'products' in data and data['products']:
        print("📦 Products:")
        for product in data['products']:
            print(f"  • {product}")
    
    if 'services' in data and data['services']:
        print("\n🔧 Services:")
        for service in data['services']:
            print(f"  • {service}")
    
    if 'confidence' in data:
        print(f"\n🎯 Confidence: {data['confidence']}")


def format_leadership(data: Dict[str, Any]) -> None:
    """Format and print leadership information."""
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
        return
    
    if not data.get('data_available', False):
        print("ℹ️  Leadership information not available")
        return
    
    if 'leadership_team' in data and data['leadership_team']:
        print("👥 Leadership Team:")
        for leader in data['leadership_team']:
            if isinstance(leader, dict):
                name = leader.get('name', 'Unknown')
                position = leader.get('position', 'Unknown Position')
                print(f"  • {name} - {position}")
                if 'background' in leader:
                    print(f"    Background: {leader['background'][:100]}...")
            else:
                print(f"  • {leader}")


def format_news(data: Dict[str, Any]) -> None:
    """Format and print company news."""
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
        return
    
    if 'news_items' in data and data['news_items']:
        print("📰 Recent News:")
        for i, news_item in enumerate(data['news_items'][:5], 1):
            if isinstance(news_item, dict):
                title = news_item.get('title', 'No title')
                date = news_item.get('date', 'Unknown date')
                print(f"  {i}. [{date}] {title}")
                if 'summary' in news_item:
                    print(f"     {news_item['summary'][:150]}...")
            else:
                print(f"  {i}. {news_item}")
    
    if 'data_confidence' in data:
        print(f"\n🎯 Data Confidence: {data['data_confidence']}")


def format_competitive_analysis(data: Dict[str, Any]) -> None:
    """Format and print competitive analysis."""
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
        return
    
    if 'main_competitors' in data and data['main_competitors']:
        print("🏆 Main Competitors:")
        for competitor in data['main_competitors']:
            print(f"  • {competitor}")
    
    if 'market_position' in data:
        print(f"\n📈 Market Position: {data['market_position']}")
    
    if 'strengths' in data and data['strengths']:
        print("\n💪 Strengths:")
        for strength in data['strengths']:
            print(f"  • {strength}")
    
    if 'weaknesses' in data and data['weaknesses']:
        print("\n⚠️  Weaknesses:")
        for weakness in data['weaknesses']:
            print(f"  • {weakness}")


def format_financials(data: Dict[str, Any]) -> None:
    """Format and print financial information."""
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
        return
    
    if not data.get('data_available', False):
        print("ℹ️  Financial information not available")
        return
    
    fin_info = data.get('financial_information', {})
    
    # Handle the new rich JSON structure from Gemini API
    if 'company' in fin_info and 'ticker' in fin_info:
        # This is the new detailed format
        print(f"📊 Company: {fin_info['company']}")
        if fin_info.get('ticker'):
            print(f"📈 Ticker: {fin_info['ticker']}")
        if fin_info.get('lastUpdated'):
            print(f"📅 Last Updated: {fin_info['lastUpdated']}")
        
        # Detailed financials
        financials = fin_info.get('financials', {})
        if financials:
            # Revenue information
            revenue = financials.get('revenue', {})
            if revenue:
                print("\n💰 Revenue:")
                latest_q = revenue.get('latestQuarter', {})
                if latest_q.get('value'):
                    value = latest_q['value']
                    period = latest_q.get('period', 'Unknown')
                    currency = latest_q.get('currency', 'USD')
                    # Format large numbers
                    if value >= 1_000_000_000:
                        formatted_value = f"{value / 1_000_000_000:.2f}B"
                    elif value >= 1_000_000:
                        formatted_value = f"{value / 1_000_000:.2f}M"
                    else:
                        formatted_value = f"{value:,}"
                    print(f"  • Latest Quarter ({period}): {currency} {formatted_value}")
            
            # Profit information
            profit = financials.get('profit', {})
            if profit:
                print("\n💵 Profit:")
                latest_q = profit.get('latestQuarter', {})
                if latest_q.get('value'):
                    value = latest_q['value']
                    period = latest_q.get('period', 'Unknown')
                    currency = latest_q.get('currency', 'USD')
                    # Format large numbers
                    if value >= 1_000_000_000:
                        formatted_value = f"{value / 1_000_000_000:.2f}B"
                    elif value >= 1_000_000:
                        formatted_value = f"{value / 1_000_000:.2f}M"
                    else:
                        formatted_value = f"{value:,}"
                    print(f"  • Latest Quarter ({period}): {currency} {formatted_value}")
            
            # Key ratios
            ratios = financials.get('keyRatios', {})
            if ratios:
                print("\n📊 Key Ratios:")
                for ratio_name, ratio_data in ratios.items():
                    if isinstance(ratio_data, dict) and ratio_data.get('value') is not None:
                        value = ratio_data['value']
                        date = ratio_data.get('asOfDate', '')
                        formatted_name = ratio_name.replace('Ratio', ' Ratio').replace('pe', 'P/E').title()
                        if date:
                            print(f"  • {formatted_name}: {value} (as of {date})")
                        else:
                            print(f"  • {formatted_name}: {value}")
        
        # Recent news
        news = fin_info.get('recentNews', [])
        if news:
            print("\n📰 Recent News:")
            for i, news_item in enumerate(news[:3], 1):  # Show max 3 news items
                if isinstance(news_item, dict):
                    headline = news_item.get('headline', 'No headline')
                    source = news_item.get('source', 'Unknown source')
                    date = news_item.get('date', '')
                    print(f"  {i}. [{date}] {headline}")
                    print(f"     Source: {source}")
    
    elif fin_info.get('public_company'):
        # Handle legacy format for public companies
        print("📈 Public Company")
        
        # Stock information
        stock_info = fin_info.get('stock_info', {})
        if stock_info:
            print("\n🏛️  Stock Information:")
            if stock_info.get('symbol'):
                print(f"  • Symbol: {stock_info['symbol']}")
            if stock_info.get('exchange'):
                print(f"  • Exchange: {stock_info['exchange']}")
            if stock_info.get('market_cap'):
                print(f"  • Market Cap: {stock_info['market_cap']}")
        
        # Financial data
        financial_data = fin_info.get('financial_data', {})
        if financial_data and isinstance(financial_data, dict):
            print("\n💰 Financial Data:")
            for key, value in financial_data.items():
                if value:  # Only show non-empty values
                    formatted_key = key.replace('_', ' ').title()
                    print(f"  • {formatted_key}: {value}")
    
    elif fin_info.get('public_company') == False:
        # Handle legacy format for private companies
        print("🏢 Private Company")
        
        # Financial data for private companies
        financial_data = fin_info.get('financial_data', {})
        if financial_data and isinstance(financial_data, dict):
            print("\n💰 Financial Information:")
            for key, value in financial_data.items():
                if value:  # Only show non-empty values
                    formatted_key = key.replace('_', ' ').title()
                    print(f"  • {formatted_key}: {value}")
    
    else:
        # Fallback for simpler financial information structure
        if fin_info:
            print("💰 Financial Information:")
            for key, value in fin_info.items():
                if value and key not in ['public_company', 'stock_info', 'financial_data']:
                    formatted_key = key.replace('_', ' ').title()
                    print(f"  • {formatted_key}: {value}")
    
    # Show data source if available
    if 'source' in data:
        print(f"\n📡 Source: {data['source']}")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Research companies using Google Gemini AI and web scraping",
        epilog="Examples:\n"
               "  %(prog)s --company 'Apple Inc.' --all\n"
               "  %(prog)s --company 'Microsoft' --exists --products\n"
               "  %(prog)s --company 'Google' --comprehensive --output report.json\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Required arguments
    parser.add_argument(
        "--company", "-c",
        type=str,
        required=True,
        help="Name of the company to research"
    )
    
    # Research type arguments
    parser.add_argument(
        "--exists", "-e",
        action="store_true",
        help="Check if company exists"
    )
    
    parser.add_argument(
        "--products", "-p",
        action="store_true",
        help="Get company products and services"
    )
    
    parser.add_argument(
        "--leadership", "-l",
        action="store_true",
        help="Get company leadership information"
    )
    
    parser.add_argument(
        "--news", "-n",
        action="store_true",
        help="Get recent company news"
    )
    
    parser.add_argument(
        "--competitive", "-comp",
        action="store_true",
        help="Get competitive analysis"
    )
    
    parser.add_argument(
        "--financials", "-f",
        action="store_true",
        help="Get financial information"
    )
    
    parser.add_argument(
        "--comprehensive", "-comp-data",
        action="store_true",
        help="Get comprehensive company data (all available information)"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all research types"
    )
    
    # Configuration arguments
    parser.add_argument(
        "--api-key",
        type=str,
        help="Google Gemini API key (can also be set via GEMINI_API_KEY env var)"
    )
    
    parser.add_argument(
        "--no-web-scraping",
        action="store_true",
        help="Disable web scraping (API only)"
    )
    
    parser.add_argument(
        "--news-limit",
        type=int,
        default=5,
        help="Number of news items to retrieve (default: 5)"
    )
    
    # Output arguments
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Save results to JSON file"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format instead of formatted text"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress section headers and formatting"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not any([args.exists, args.products, args.leadership, args.news, 
                args.competitive, args.financials, args.comprehensive, args.all]):
        parser.error("You must specify at least one research type. Use --help for options.")
    
    try:
        # Initialize the researcher
        researcher = CompanyResearcher(
            api_key=args.api_key,
            use_web_scraping=not args.no_web_scraping
        )
        
        company_name = args.company
        results = {}
        
        if not args.quiet:
            print(f"🔍 Researching: {company_name}")
        
        # Run requested research types
        if args.all or args.exists:
            if not args.quiet:
                print_section_header("Company Existence Check")
            
            result = researcher.check_company_exists(company_name)
            results['existence'] = result
            
            if args.json:
                print_json_pretty(result)
            else:
                format_existence_check(result)
        
        if args.all or args.products:
            if not args.quiet:
                print_section_header("Products & Services")
            
            result = researcher.get_company_products_services(company_name)
            results['products_services'] = result
            
            if args.json:
                print_json_pretty(result)
            else:
                format_products_services(result)
        
        if args.all or args.leadership:
            if not args.quiet:
                print_section_header("Leadership Information")
            
            result = researcher.get_company_leadership(company_name)
            results['leadership'] = result
            
            if args.json:
                print_json_pretty(result)
            else:
                format_leadership(result)
        
        if args.all or args.news:
            if not args.quiet:
                print_section_header("Recent News")
            
            result = researcher.get_company_news(company_name, limit=args.news_limit)
            results['news'] = result
            
            if args.json:
                print_json_pretty(result)
            else:
                format_news(result)
        
        if args.all or args.competitive:
            if not args.quiet:
                print_section_header("Competitive Analysis")
            
            result = researcher.get_competitive_analysis(company_name)
            results['competitive_analysis'] = result
            
            if args.json:
                print_json_pretty(result)
            else:
                format_competitive_analysis(result)
        
        if args.all or args.financials:
            if not args.quiet:
                print_section_header("Financial Information")
            
            result = researcher.get_company_financials(company_name)
            results['financials'] = result
            
            if args.json:
                print_json_pretty(result)
            else:
                format_financials(result)
        
        if args.comprehensive:
            if not args.quiet:
                print_section_header("Comprehensive Company Data")
            
            result = researcher.get_company_data(company_name)
            results['comprehensive'] = result
            
            if args.json:
                print_json_pretty(result)
            else:
                format_company_summary(result)
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            if not args.quiet:
                print(f"\n💾 Results saved to: {args.output}")
        
        if not args.quiet:
            print("\n✅ Research completed successfully!")
    
    except KeyboardInterrupt:
        print("\n❌ Research interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error during research: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
