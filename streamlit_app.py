#!/usr/bin/env python
"""
Company Research Tool - Streamlit Web Interface

A web-based interface for researching companies using Google's Gemini AI and web scraping.
"""

import streamlit as st
import json
import sys
import os
from typing import Dict, Any, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from src.company_researcher import CompanyResearcher

# Page configuration
st.set_page_config(
    page_title="Company Research Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .domain-input {
        margin: 0.5rem 0;
        padding: 0.5rem;
        border: 1px solid #e0e0e0;
        border-radius: 0.25rem;
    }
    .domain-list {
        max-height: 200px;
        overflow-y: auto;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables."""
    if 'research_results' not in st.session_state:
        st.session_state.research_results = {}
    if 'api_key_set' not in st.session_state:
        st.session_state.api_key_set = False
    if 'researcher' not in st.session_state:
        st.session_state.researcher = None
    if 'domains' not in st.session_state:
        st.session_state.domains = []
    if 'last_research_company' not in st.session_state:
        st.session_state.last_research_company = None
    if 'show_download_section' not in st.session_state:
        st.session_state.show_download_section = False

def setup_api_key():
    """Setup API key from environment or user input."""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        st.sidebar.markdown("### 🔑 API Configuration")
        api_key = st.sidebar.text_input(
            "Enter your Google Gemini API key:",
            type="password",
            help="Get your API key from https://ai.google.dev/"
        )
        
        if api_key:
            st.session_state.api_key_set = True
            return api_key
        else:
            st.sidebar.error("Please enter your Gemini API key to continue.")
            return None
    else:
        st.session_state.api_key_set = True
        return api_key

def create_researcher(api_key: str, use_web_scraping: bool = True) -> CompanyResearcher:
    """Create and cache the CompanyResearcher instance."""
    alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')
    if (st.session_state.researcher is None or 
        getattr(st.session_state.researcher, 'use_web_scraping', True) != use_web_scraping):
        st.session_state.researcher = CompanyResearcher(
            api_key=api_key,
            use_web_scraping=use_web_scraping,
            alpha_vantage_key=alpha_vantage_key
        )
    return st.session_state.researcher

def format_financial_data(financial_info: Dict[str, Any]) -> None:
    """Format and display financial information."""
    if not financial_info or not financial_info.get('data_available', False):
        st.warning("📊 Financial information not available")
        return
    
    fin_data = financial_info.get('financial_information', {})
    
    # Handle new enhanced format
    if 'company' in fin_data and 'financials' in fin_data:
        st.subheader(f"💰 Financial Information - {fin_data['company']}")
        
        if fin_data.get('ticker'):
            st.info(f"📈 **Ticker:** {fin_data['ticker']}")
        
        financials = fin_data.get('financials', {})
        
        # Create metrics columns
        col1, col2, col3 = st.columns(3)
        
        # Revenue
        revenue = financials.get('revenue', {}).get('latestQuarter', {})
        if revenue.get('value'):
            value = revenue['value']
            if value >= 1_000_000_000:
                formatted_value = f"${value / 1_000_000_000:.2f}B"
            elif value >= 1_000_000:
                formatted_value = f"${value / 1_000_000:.2f}M"
            else:
                formatted_value = f"${value:,.0f}"
            
            col1.metric(
                "Revenue (Latest Quarter)",
                formatted_value,
                delta=revenue.get('period', '')
            )
        
        # Profit
        profit = financials.get('profit', {}).get('latestQuarter', {})
        if profit.get('value'):
            value = profit['value']
            if value >= 1_000_000_000:
                formatted_value = f"${value / 1_000_000_000:.2f}B"
            elif value >= 1_000_000:
                formatted_value = f"${value / 1_000_000:.2f}M"
            else:
                formatted_value = f"${value:,.0f}"
            
            col2.metric(
                "Profit (Latest Quarter)",
                formatted_value,
                delta=profit.get('period', '')
            )
        
        # Key ratios
        ratios = financials.get('keyRatios', {})
        if ratios:
            pe_ratio = ratios.get('peRatio', {}).get('value')
            if pe_ratio:
                col3.metric("P/E Ratio", f"{pe_ratio:.2f}")
        
        # Recent news
        news = fin_data.get('recentNews', [])
        if news:
            st.subheader("📰 Recent Financial News")
            for i, news_item in enumerate(news[:3], 1):
                if isinstance(news_item, dict):
                    headline = news_item.get('headline', 'No headline')
                    source = news_item.get('source', 'Unknown source')
                    date = news_item.get('date', '')
                    
                    with st.expander(f"{i}. {headline}"):
                        st.write(f"**Source:** {source}")
                        if date:
                            st.write(f"**Date:** {date}")

def display_company_existence(data: Dict[str, Any]) -> None:
    """Display company existence check results."""
    if 'error' in data:
        st.error(f"❌ Error: {data['error']}")
        return
    
    exists = data.get('exists', 'Unknown')
    
    if exists == 'Yes':
        st.success("✅ Company exists and is verified")
    elif exists == 'No':
        st.error("❌ Company does not exist or could not be verified")
    else:
        st.warning(f"❓ Status: {exists}")
    
    if 'industry' in data:
        st.info(f"🏭 **Industry:** {data['industry']}")
    
    if 'reason' in data:
        st.write(f"💭 **Details:** {data['reason']}")

def display_products_services(data: Dict[str, Any]) -> None:
    """Display products and services information."""
    if 'error' in data:
        st.error(f"❌ Error: {data['error']}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'products' in data and data['products']:
            st.subheader("📦 Products")
            for product in data['products']:
                st.write(f"• {product}")
    
    with col2:
        if 'services' in data and data['services']:
            st.subheader("🔧 Services")
            for service in data['services']:
                st.write(f"• {service}")
    
    if 'confidence' in data:
        st.info(f"🎯 **Confidence Level:** {data['confidence']}")

def display_leadership(data: Dict[str, Any]) -> None:
    """Display leadership information."""
    if 'error' in data:
        st.error(f"❌ Error: {data['error']}")
        return
    
    if not data.get('data_available', False):
        st.warning("ℹ️ Leadership information not available")
        return
    
    if 'leadership_team' in data and data['leadership_team']:
        st.subheader("👥 Leadership Team")
        
        for leader in data['leadership_team']:
            if isinstance(leader, dict):
                name = leader.get('name', 'Unknown')
                position = leader.get('position', 'Unknown Position')
                
                with st.expander(f"{name} - {position}"):
                    if 'background' in leader:
                        st.write(f"**Background:** {leader['background']}")
            else:
                st.write(f"• {leader}")

def display_news(data: Dict[str, Any]) -> None:
    """Display company news."""
    if 'error' in data:
        st.error(f"❌ Error: {data['error']}")
        return
    
    if 'news_items' in data and data['news_items']:
        st.subheader("📰 Recent News")
        
        for i, news_item in enumerate(data['news_items'], 1):
            if isinstance(news_item, dict):
                title = news_item.get('title', 'No title')
                date = news_item.get('date', 'Unknown date')
                summary = news_item.get('summary', '')
                
                with st.expander(f"{i}. [{date}] {title}"):
                    if summary:
                        st.write(summary)
            else:
                st.write(f"{i}. {news_item}")

def display_competitive_analysis(data: Dict[str, Any]) -> None:
    """Display competitive analysis."""
    if 'error' in data:
        st.error(f"❌ Error: {data['error']}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'main_competitors' in data and data['main_competitors']:
            st.subheader("🏆 Main Competitors")
            for competitor in data['main_competitors']:
                st.write(f"• {competitor}")
        
        if 'market_position' in data:
            st.info(f"📈 **Market Position:** {data['market_position']}")
    
    with col2:
        if 'strengths' in data and data['strengths']:
            st.subheader("💪 Strengths")
            for strength in data['strengths']:
                st.write(f"• {strength}")
        
        if 'weaknesses' in data and data['weaknesses']:
            st.subheader("⚠️ Weaknesses")
            for weakness in data['weaknesses']:
                st.write(f"• {weakness}")

def create_summary_dashboard(results: Dict[str, Any], company_name: str) -> None:
    """Create a summary dashboard with key metrics."""
    st.header(f"📊 {company_name} - Summary Dashboard")
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Company existence
    exists_data = results.get('existence', {})
    exists = exists_data.get('exists', 'Unknown')
    col1.metric("Company Status", "✅ Verified" if exists == 'Yes' else "❓ Unverified")
    
    # Industry
    industry = exists_data.get('industry', 'Unknown')
    col2.metric("Industry", industry)
    
    # Data sources count
    total_sources = len([k for k in results.keys() if results[k] and not results[k].get('error')])
    col3.metric("Data Sources", f"{total_sources}/6")
    
    # Financial status
    fin_data = results.get('financials', {})
    fin_status = "Available" if fin_data.get('data_available') else "Limited"
    col4.metric("Financial Data", fin_status)
    
    # Create tabs for detailed information
    tabs = st.tabs([
        "📋 Overview", "📦 Products/Services", "👥 Leadership", 
        "📰 News", "🏆 Competition", "💰 Financials"
    ])
    
    with tabs[0]:  # Overview
        if 'comprehensive' in results:
            data = results['comprehensive']
            st.write(f"**Company:** {data.get('company_name', company_name)}")
            st.write(f"**Industry:** {data.get('industry', 'Unknown')}")
            st.write(f"**Description:** {data.get('description', 'N/A')}")
            
            if 'data_sources' in data:
                st.write(f"**Data Sources:** {', '.join(data['data_sources'])}")
    
    with tabs[1]:  # Products/Services
        if 'products_services' in results:
            display_products_services(results['products_services'])
    
    with tabs[2]:  # Leadership
        if 'leadership' in results:
            display_leadership(results['leadership'])
    
    with tabs[3]:  # News
        if 'news' in results:
            display_news(results['news'])
    
    with tabs[4]:  # Competition
        if 'competitive_analysis' in results:
            display_competitive_analysis(results['competitive_analysis'])
    
    with tabs[5]:  # Financials
        if 'financials' in results:
            format_financial_data(results['financials'])

def manage_domains():
    """Domain management section in the sidebar."""
    st.sidebar.markdown("### 🌐 Domain Management")
    
    # Single domain input
    new_domain = st.sidebar.text_input(
        "Add Domain:",
        placeholder="e.g., example.com",
        help="Enter a domain name without http:// or www"
    )
    
    # Bulk domain input
    st.sidebar.markdown("#### Bulk Add Domains")
    bulk_domains = st.sidebar.text_area(
        "Add Multiple Domains:",
        placeholder="Enter domains separated by commas or new lines",
        help="Enter multiple domains separated by commas or new lines"
    )
    
    # Add domain button
    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        if st.button("Add Domain", key="add_single_domain"):
            if new_domain:
                if new_domain not in st.session_state.domains:
                    st.session_state.domains.append(new_domain.strip())
                    st.success(f"Added domain: {new_domain}")
                else:
                    st.warning("Domain already exists!")
    
    with col2:
        if st.button("Add Bulk", key="add_bulk_domains"):
            if bulk_domains:
                # Split by commas and newlines
                new_domains = [d.strip() for d in bulk_domains.replace('\n', ',').split(',')]
                new_domains = [d for d in new_domains if d]  # Remove empty strings
                
                # Add unique domains
                added = 0
                for domain in new_domains:
                    if domain not in st.session_state.domains:
                        st.session_state.domains.append(domain)
                        added += 1
                
                if added > 0:
                    st.success(f"Added {added} new domain(s)")
                else:
                    st.info("No new domains to add")
    
    # Display and manage current domains
    if st.session_state.domains:
        st.sidebar.markdown("#### Current Domains")
        for i, domain in enumerate(st.session_state.domains):
            col1, col2 = st.sidebar.columns([3, 1])
            with col1:
                st.text(domain)
            with col2:
                if st.button("🗑️", key=f"remove_{i}"):
                    st.session_state.domains.pop(i)
                    st.rerun()
        
        if st.sidebar.button("Clear All Domains"):
            st.session_state.domains = []
            st.rerun()
    
    return st.session_state.domains

def display_comprehensive_data(data: Dict[str, Any]) -> None:
    """Display comprehensive company data."""
    if 'error' in data:
        st.error(f"❌ Error: {data['error']}")
    else:
        st.write(f"**Company:** {data.get('company_name', 'N/A')}")
        st.write(f"**Industry:** {data.get('industry', 'N/A')}")
        st.write(f"**Description:** {data.get('description', 'N/A')}")
        
        if 'websites_checked' in data:
            st.subheader("🌐 Websites Analyzed")
            for website in data['websites_checked']:
                status = "✅" if website['success'] else "❌"
                st.write(f"{status} {website['domain']}")
        
        if 'data_sources' in data:
            st.write(f"**Data Sources:** {', '.join(data['data_sources'])}")

def main():
    """Main Streamlit application."""
    init_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🔍 Company Research Tool</h1>', unsafe_allow_html=True)
    st.markdown("**Powered by Google Gemini AI and Web Scraping**")
    
    # Setup API key
    api_key = setup_api_key()
    
    if not api_key:
        st.warning("Please configure your Google Gemini API key to continue.")
        st.info("💡 **Tip:** You can also set the `GEMINI_API_KEY` environment variable.")
        return
    
    # Sidebar configuration
    st.sidebar.markdown("### ⚙️ Research Configuration")
    
    # Company input
    company_name = st.sidebar.text_input(
        "🏢 Company Name:",
        placeholder="e.g., Apple Inc., Microsoft Corporation",
        help="Enter the full company name for best results"
    )
    
    # Domain management
    domains = manage_domains()
    
    # Research options
    st.sidebar.markdown("### 📊 Research Types")
    research_options = {
        'existence': st.sidebar.checkbox("🔍 Company Existence", value=True),
        'products_services': st.sidebar.checkbox("📦 Products & Services"),
        'leadership': st.sidebar.checkbox("👥 Leadership"),
        'news': st.sidebar.checkbox("📰 Recent News"),
        'competitive_analysis': st.sidebar.checkbox("🏆 Competitive Analysis"),
        'financials': st.sidebar.checkbox("💰 Financial Information"),
        'comprehensive': st.sidebar.checkbox("📋 Comprehensive Data")
    }
    
    # Advanced options
    st.sidebar.markdown("### 🔧 Advanced Options")
    use_web_scraping = st.sidebar.checkbox("🌐 Enable Web Scraping", value=True)
    news_limit = st.sidebar.slider("📰 News Items Limit", 1, 20, 5)
    
    # Research button
    research_button = st.sidebar.button("🚀 Start Research", type="primary")
    
    # Main content area
    if research_button and company_name:
        if not any(research_options.values()):
            st.error("Please select at least one research type.")
            return
        
        # Create researcher
        try:
            researcher = create_researcher(api_key, use_web_scraping)
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = {}
            total_tasks = sum(research_options.values())
            completed_tasks = 0
            
            # Execute research tasks
            if research_options['existence']:
                status_text.text("🔍 Checking company existence...")
                results['existence'] = researcher.check_company_exists(company_name)
                completed_tasks += 1
                progress_bar.progress(completed_tasks / total_tasks)
            
            if research_options['products_services']:
                status_text.text("📦 Extracting products and services...")
                results['products_services'] = researcher.get_company_products_services(company_name)
                completed_tasks += 1
                progress_bar.progress(completed_tasks / total_tasks)
            
            if research_options['leadership']:
                status_text.text("👥 Gathering leadership information...")
                results['leadership'] = researcher.get_company_leadership(company_name)
                completed_tasks += 1
                progress_bar.progress(completed_tasks / total_tasks)
            
            if research_options['news']:
                status_text.text("📰 Collecting recent news...")
                results['news'] = researcher.get_company_news(company_name, limit=news_limit)
                completed_tasks += 1
                progress_bar.progress(completed_tasks / total_tasks)
            
            if research_options['competitive_analysis']:
                status_text.text("🏆 Analyzing competition...")
                results['competitive_analysis'] = researcher.get_competitive_analysis(company_name)
                completed_tasks += 1
                progress_bar.progress(completed_tasks / total_tasks)
            
            if research_options['financials']:
                status_text.text("💰 Extracting financial data...")
                # Pass all configured domains to the financial extractor
                results['financials'] = researcher.get_company_financials(company_name, domain=domains[0] if domains else None)
                completed_tasks += 1
                progress_bar.progress(completed_tasks / total_tasks)
            
            if research_options['comprehensive']:
                status_text.text("📋 Compiling comprehensive data...")
                results['comprehensive'] = researcher.get_company_data(company_name)
                completed_tasks += 1
                progress_bar.progress(completed_tasks / total_tasks)
            
            # Complete
            progress_bar.progress(1.0)
            status_text.text("✅ Research completed!")
            
            # Store results and enable download section
            st.session_state.research_results[company_name] = results
            st.session_state.last_research_company = company_name
            
            # Display results
            st.success(f"✅ Research completed for **{company_name}**!")
            
            # Show summary dashboard if multiple research types
            if sum(research_options.values()) > 1:
                create_summary_dashboard(results, company_name)
            else:
                # Show individual results
                for research_type, data in results.items():
                    if research_type == 'existence':
                        st.header("🔍 Company Existence Check")
                        display_company_existence(data)
                    elif research_type == 'products_services':
                        st.header("📦 Products & Services")
                        display_products_services(data)
                    elif research_type == 'leadership':
                        st.header("👥 Leadership Information")
                        display_leadership(data)
                    elif research_type == 'news':
                        st.header("📰 Recent News")
                        display_news(data)
                    elif research_type == 'competitive_analysis':
                        st.header("🏆 Competitive Analysis")
                        display_competitive_analysis(data)
                    elif research_type == 'financials':
                        st.header("💰 Financial Information")
                        format_financial_data(data)
                    elif research_type == 'comprehensive':
                        st.header("📋 Comprehensive Company Data")
                        display_comprehensive_data(data)
        
        except Exception as e:
            st.error(f"❌ An error occurred during research: {str(e)}")
            st.error("Please check your API key and internet connection.")
    
    elif research_button and not company_name:
        st.error("Please enter a company name.")
    
    # Previous research results
    if st.session_state.research_results:
        st.markdown("---")
        st.subheader("📚 Previous Research Results")
        
        selected_company = st.selectbox(
            "Select a previously researched company:",
            list(st.session_state.research_results.keys()),
            key="previous_company_selector"
        )
        
        if selected_company:
            st.write(f"**Selected:** {selected_company}")
            
            # Show the dashboard for selected company
            results = st.session_state.research_results[selected_company]
            create_summary_dashboard(results, selected_company)
    
    # Show Downloads button (when results available but download section not shown)
    if (st.session_state.research_results and 
        not st.session_state.show_download_section and 
        st.session_state.last_research_company):
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("📥 Show Downloads", key="show_downloads_main"):
                st.session_state.show_download_section = True
                st.rerun()
    
    # Persistent download section (always at the bottom for consistent positioning)
    if st.session_state.show_download_section and st.session_state.last_research_company:
        company_name = st.session_state.last_research_company
        results = st.session_state.research_results.get(company_name, {})
        
        if results:
            st.markdown("---")
            st.markdown(f"### 💾 Download Results for {company_name}")
            st.info("💡 **Tip:** Download buttons remain available until you start a new research.")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                json_data = json.dumps(results, indent=2, ensure_ascii=False)
                st.download_button(
                    label="📄 Download JSON",
                    data=json_data,
                    file_name=f"{company_name.replace(' ', '_')}_research.json",
                    mime="application/json",
                    key=f"json_download_{company_name}",  # Unique key to prevent conflicts
                    help="Download complete research data as JSON file"
                )
            
            with col2:
                # Create a simple CSV for basic data
                csv_data = []
                for research_type, data in results.items():
                    if isinstance(data, dict) and 'error' not in data:
                        csv_data.append({
                            'Research_Type': research_type,
                            'Data_Available': data.get('data_available', True),
                            'Summary': str(data)[:100] + '...' if len(str(data)) > 100 else str(data)
                        })
                
                if csv_data:
                    df = pd.DataFrame(csv_data)
                    csv_string = df.to_csv(index=False)
                    st.download_button(
                        label="📊 Download CSV",
                        data=csv_string,
                        file_name=f"{company_name.replace(' ', '_')}_research.csv",
                        mime="text/csv",
                        key=f"csv_download_{company_name}",  # Unique key to prevent conflicts
                        help="Download summary data as CSV file"
                    )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Company Research Tool** | Powered by Google Gemini AI | "
        "Built with ❤️ using Streamlit"
    )

if __name__ == "__main__":
    main()
