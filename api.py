#!/usr/bin/env python3
"""
FastAPI REST API for Company Research Tool

This module provides a REST API interface for the Company Research Tool,
exposing all research capabilities through HTTP endpoints.
"""

import os
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

from src.company_researcher import CompanyResearcher
from src import get_version

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response validation
class CompanyExistenceResponse(BaseModel):
    """Response model for company existence check"""
    exists: str = Field(..., description="Whether the company exists (Yes/No/Unclear)")
    reason: Optional[str] = Field(None, description="Reason for the conclusion")
    industry: Optional[str] = Field(None, description="Industry if company exists")
    website_found: Optional[bool] = Field(None, description="Whether a website was found")
    website: Optional[str] = Field(None, description="Company website URL")
    domain: Optional[str] = Field(None, description="Company domain")

class ProductsServicesResponse(BaseModel):
    """Response model for products and services"""
    products: Optional[list] = Field(None, description="List of company products")
    services: Optional[list] = Field(None, description="List of company services")
    confidence: Optional[str] = Field(None, description="Confidence level of the data")
    business_model: Optional[str] = Field(None, description="Business model description")
    target_market: Optional[str] = Field(None, description="Target market information")

class LeadershipResponse(BaseModel):
    """Response model for leadership information"""
    data_available: Optional[bool] = Field(None, description="Whether leadership data is available")
    leadership_team: Optional[list] = Field(None, description="List of leadership team members")
    key_executives: Optional[list] = Field(None, description="Key executives information")
    board_members: Optional[list] = Field(None, description="Board members if available")
    confidence: Optional[str] = Field(None, description="Confidence level of the data")

class NewsResponse(BaseModel):
    """Response model for company news"""
    news_items: Optional[list] = Field(None, description="List of recent news items")
    data_confidence: Optional[str] = Field(None, description="Confidence level of the data")
    total_count: Optional[int] = Field(None, description="Total number of news items found")
    search_timestamp: Optional[str] = Field(None, description="When the search was performed")

class CompetitiveAnalysisResponse(BaseModel):
    """Response model for competitive analysis"""
    main_competitors: Optional[list] = Field(None, description="List of main competitors")
    market_position: Optional[str] = Field(None, description="Company's market position")
    strengths: Optional[list] = Field(None, description="Company strengths")
    weaknesses: Optional[list] = Field(None, description="Company weaknesses")
    competitive_advantages: Optional[list] = Field(None, description="Competitive advantages")
    market_analysis: Optional[Dict[str, Any]] = Field(None, description="Market analysis data")

class FinancialsResponse(BaseModel):
    """Response model for financial information"""
    data_available: Optional[bool] = Field(None, description="Whether financial data is available")
    financial_information: Optional[Dict[str, Any]] = Field(None, description="Financial data")
    source: Optional[str] = Field(None, description="Data source")

class CompanyDataResponse(BaseModel):
    """Response model for comprehensive company data"""
    company_name: Optional[str] = Field(None, description="Company name")
    exists: Optional[bool] = Field(None, description="Whether company exists")
    description: Optional[str] = Field(None, description="Company description")
    industry: Optional[str] = Field(None, description="Company industry")
    data_confidence: Optional[str] = Field(None, description="Data confidence level")
    data_sources: Optional[list] = Field(None, description="Data sources")
    # Allow any additional fields
    class Config:
        extra = "allow"

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")

# Initialize FastAPI app
app = FastAPI(
    title="Company Research Tool API",
    description="REST API for comprehensive company research and analysis",
    version=get_version(),
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the company researcher
researcher = None

@app.on_event("startup")
async def startup_event():
    """Initialize the company researcher on startup"""
    global researcher
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
        
        researcher = CompanyResearcher(api_key=api_key, use_web_scraping=True)
        logger.info("Company Research Tool API started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Company Researcher: {e}")
        raise

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Company Research Tool API",
        "version": get_version(),
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": get_version()}

@app.get("/companies/{company_name}/exists", 
         response_model=CompanyExistenceResponse,
         summary="Check if company exists",
         description="Verify if a company exists and get basic information")
async def check_company_exists(
    company_name: str = Path(..., description="Name of the company to check", min_length=1)
):
    """Check if a company exists"""
    try:
        if not researcher:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        result = researcher.check_company_exists(company_name)
        return result  # Return raw result, Pydantic will validate and convert
    except Exception as e:
        logger.error(f"Error checking company existence for {company_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/companies/{company_name}/products-services",
         response_model=ProductsServicesResponse,
         summary="Get company products and services",
         description="Retrieve information about company's products and services")
async def get_products_services(
    company_name: str = Path(..., description="Name of the company", min_length=1)
):
    """Get company products and services"""
    try:
        if not researcher:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        result = researcher.get_company_products_services(company_name)
        return result
    except Exception as e:
        logger.error(f"Error getting products/services for {company_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/companies/{company_name}/leadership",
         response_model=LeadershipResponse,
         summary="Get company leadership",
         description="Retrieve information about company's leadership team")
async def get_leadership(
    company_name: str = Path(..., description="Name of the company", min_length=1),
    domain: Optional[str] = Query(None, description="Company website domain (optional)")
):
    """Get company leadership information"""
    try:
        if not researcher:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        result = researcher.get_company_leadership(company_name, domain)
        return result
    except Exception as e:
        logger.error(f"Error getting leadership for {company_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/companies/{company_name}/news",
         response_model=NewsResponse,
         summary="Get company news",
         description="Retrieve recent news about the company")
async def get_news(
    company_name: str = Path(..., description="Name of the company", min_length=1),
    limit: int = Query(5, description="Maximum number of news items to return", ge=1, le=20)
):
    """Get company news"""
    try:
        if not researcher:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        result = researcher.get_company_news(company_name, limit)
        return result
    except Exception as e:
        logger.error(f"Error getting news for {company_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/companies/{company_name}/competitive-analysis",
         response_model=CompetitiveAnalysisResponse,
         summary="Get competitive analysis",
         description="Retrieve competitive analysis for the company")
async def get_competitive_analysis(
    company_name: str = Path(..., description="Name of the company", min_length=1)
):
    """Get competitive analysis"""
    try:
        if not researcher:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        result = researcher.get_competitive_analysis(company_name)
        return result
    except Exception as e:
        logger.error(f"Error getting competitive analysis for {company_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/companies/{company_name}/financials",
         response_model=FinancialsResponse,
         summary="Get company financials",
         description="Retrieve financial information about the company")
async def get_financials(
    company_name: str = Path(..., description="Name of the company", min_length=1),
    domain: Optional[str] = Query(None, description="Company website domain (optional)")
):
    """Get company financial information"""
    try:
        if not researcher:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        result = researcher.get_company_financials(company_name, domain)
        return result
    except Exception as e:
        logger.error(f"Error getting financials for {company_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/companies/{company_name}/comprehensive",
         response_model=CompanyDataResponse,
         summary="Get comprehensive company data",
         description="Retrieve all available information about the company")
async def get_comprehensive_data(
    company_name: str = Path(..., description="Name of the company", min_length=1)
):
    """Get comprehensive company data"""
    try:
        if not researcher:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        result = researcher.get_company_data(company_name)
        return result
    except Exception as e:
        logger.error(f"Error getting comprehensive data for {company_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.detail).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )

if __name__ == "__main__":
    # Configuration for development
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting Company Research Tool API on {host}:{port}")
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
