"""Financial dashboard component for Streamlit interface."""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any

def format_currency(value: float, currency: str = "USD") -> str:
    """Format currency values with appropriate suffixes (K, M, B)."""
    if value is None:
        return "N/A"
    
    suffixes = ["", "K", "M", "B", "T"]
    magnitude = 0
    while abs(value) >= 1000 and magnitude < len(suffixes)-1:
        value /= 1000
        magnitude += 1
    return f"{value:.2f}{suffixes[magnitude]} {currency}"

def create_metric_card(label: str, value: Any, delta: float = None):
    """Create a metric card with optional delta."""
    if delta:
        st.metric(label, value, delta)
    else:
        st.metric(label, value)

def display_market_data(market_data: Dict[str, Any]):
    """Display real-time market data."""
    if not market_data:
        st.warning("No market data available")
        return
    
    st.subheader("📊 Market Data")
    
    # Create three columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_metric_card(
            "Current Price",
            format_currency(market_data.get("current_price"), market_data.get("currency", "USD"))
        )
        
    with col2:
        create_metric_card(
            "Market Cap",
            format_currency(market_data.get("market_cap"), market_data.get("currency", "USD"))
        )
        
    with col3:
        create_metric_card(
            "P/E Ratio",
            f"{market_data.get('pe_ratio', 'N/A'):.2f}" if market_data.get('pe_ratio') else "N/A"
        )
    
    # Second row of metrics
    col4, col5, col6 = st.columns(3)
    
    with col4:
        create_metric_card(
            "Dividend Yield",
            f"{market_data.get('dividend_yield', 0)*100:.2f}%" if market_data.get('dividend_yield') else "N/A"
        )
        
    with col5:
        create_metric_card(
            "Volume",
            format_currency(market_data.get("volume", 0), "")
        )
        
    with col6:
        create_metric_card(
            "Avg Volume",
            format_currency(market_data.get("avg_volume", 0), "")
        )
    
    # 52-week range chart
    if all(key in market_data for key in ["fifty_two_week_low", "fifty_two_week_high", "current_price"]):
        st.subheader("52-Week Range")
        
        fig = go.Figure(go.Indicator(
            mode = "number+gauge+delta",
            value = market_data["current_price"],
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {
                    'range': [
                        market_data["fifty_two_week_low"],
                        market_data["fifty_two_week_high"]
                    ]
                },
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [market_data["fifty_two_week_low"], market_data["current_price"]], 'color': "lightgray"},
                    {'range': [market_data["current_price"], market_data["fifty_two_week_high"]], 'color': "gray"}
                ]
            }
        ))
        
        fig.update_layout(height=200)
        st.plotly_chart(fig, use_container_width=True)

def display_financial_statements(statements: Dict[str, Any]):
    """Display financial statements data."""
    if not statements:
        st.warning("No financial statements available")
        return
    
    st.subheader("📑 Financial Statements")
    
    tabs = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
    
    with tabs[0]:
        if statements.get("income_statement"):
            st.dataframe(statements["income_statement"])
        else:
            st.info("No income statement data available")
    
    with tabs[1]:
        if statements.get("balance_sheet"):
            st.dataframe(statements["balance_sheet"])
        else:
            st.info("No balance sheet data available")
    
    with tabs[2]:
        if statements.get("cash_flow"):
            st.dataframe(statements["cash_flow"])
        else:
            st.info("No cash flow data available")



def display_financial_dashboard(financial_data: Dict[str, Any]):
    """Main function to display the financial dashboard."""
    if not financial_data.get("data_available", False):
        st.warning("No financial data available for this company")
        return
    
    fin_info = financial_data.get("financial_information", {})
    
    # Display market data
    if "market_data" in fin_info:
        display_market_data(fin_info["market_data"])
    
    # Display financial statements
    if "statements" in fin_info:
        display_financial_statements(fin_info["statements"])
      # Display web-scraped data if available
    if "web_data" in fin_info:
        st.subheader("🌐 Additional Financial Information")
        
        # Create tabs for each domain
        if isinstance(fin_info["web_data"], dict):
            domains = list(fin_info["web_data"].keys())
            if domains:
                tabs = st.tabs([f"📊 {domain}" for domain in domains])
                for tab, domain in zip(tabs, domains):
                    with tab:
                        st.markdown(f"### Data from {domain}")
                        domain_data = fin_info["web_data"][domain]
                        
                        # Display domain-specific financial metrics
                        if isinstance(domain_data, dict):
                            cols = st.columns(2)
                            for i, (key, value) in enumerate(domain_data.items()):
                                with cols[i % 2]:
                                    st.metric(
                                        label=key.replace("_", " ").title(),
                                        value=value if isinstance(value, (int, float)) else str(value)
                                    )
                        else:
                            st.json(domain_data)
            else:
                st.info("No domain-specific data available")
        else:
            st.json(fin_info["web_data"])
