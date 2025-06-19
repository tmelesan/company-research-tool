"""Financial data service for retrieving real-time market data."""

import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class FinancialService:
    def __init__(self, alpha_vantage_key: str = None):
        """
        Initialize with empty state. Dependencies will be imported on demand.
        
        Args:
            alpha_vantage_key (str): Alpha Vantage API key
        """
        self.alpha_vantage_key = alpha_vantage_key or os.getenv('ALPHA_VANTAGE_KEY')
        self._yf = None
        self._av_fd = None
        self._av_ts = None
    
    def _init_yfinance(self):
        """Initialize yfinance on first use."""
        if self._yf is None:
            try:
                import yfinance as yf
                self._yf = yf
            except ImportError:
                logger.warning("yfinance not installed. Some features will be unavailable.")
                return False
        return True
    
    def _init_alpha_vantage(self):
        """Initialize Alpha Vantage on first use."""
        if self._av_fd is None and self.alpha_vantage_key:
            try:
                from alpha_vantage.fundamentaldata import FundamentalData
                from alpha_vantage.timeseries import TimeSeries
                self._av_fd = FundamentalData(key=self.alpha_vantage_key)
                self._av_ts = TimeSeries(key=self.alpha_vantage_key)
            except ImportError:
                logger.warning("alpha_vantage not installed. Some features will be unavailable.")
                return False
        return bool(self._av_fd and self._av_ts)
    
    def get_stock_info(self, ticker: str) -> Dict[str, Any]:
        """
        Get basic stock information using yfinance.
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            dict: Stock information
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                "current_price": info.get("currentPrice"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
                "volume": info.get("volume"),
                "avg_volume": info.get("averageVolume"),
                "currency": info.get("currency")
            }
        except Exception as e:
            logger.error(f"Error fetching stock info for {ticker}: {e}")
            return {}
    
    def get_financial_statements(self, ticker: str) -> Dict[str, Any]:
        """
        Get financial statements using Alpha Vantage.
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            dict: Financial statements data
        """
        if not self.alpha_vantage_key:
            logger.warning("Alpha Vantage API key not provided")
            return {}
        
        try:
            income_statement, _ = self.fd.get_income_statement_annual(ticker)
            balance_sheet, _ = self.fd.get_balance_sheet_annual(ticker)
            cash_flow, _ = self.fd.get_cash_flow_annual(ticker)
            
            return {
                "income_statement": income_statement,
                "balance_sheet": balance_sheet,
                "cash_flow": cash_flow
            }
        except Exception as e:
            logger.error(f"Error fetching financial statements for {ticker}: {e}")
            return {}
    
    def get_real_time_price(self, ticker: str) -> Optional[float]:
        """
        Get real-time stock price using Alpha Vantage.
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            float: Current stock price
        """
        if not self.alpha_vantage_key:
            return None
        
        try:
            data, _ = self.ts.get_quote_endpoint(ticker)
            return float(data.get("05. price", 0))
        except Exception as e:
            logger.error(f"Error fetching real-time price for {ticker}: {e}")
            return None
