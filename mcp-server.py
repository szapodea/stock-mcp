#!/usr/bin/env python3
"""
Simple Financial Modeling Prep MCP Server using FastMCP
Two basic functions: get stock quote and get company profile
"""

import os
import requests
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Financial Data Server")

# Get API key from environment variable
API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"


def make_fmp_request(endpoint: str) -> dict:
    """Helper function to make requests to FMP API"""
    if not API_KEY:
        return {"error": "FMP_API_KEY environment variable not set"}

    url = f"{BASE_URL}/{endpoint}"
    params = {"apikey": API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}


@mcp.tool()
def get_stock_quote(symbol: str) -> str:
    """
    Get current stock quote for a given symbol

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)

    Returns:
        Formatted string with current stock price and basic info
    """
    symbol = symbol.upper().strip()

    # Make API request
    data = make_fmp_request(f"quote/{symbol}")

    # Handle errors
    if "error" in data:
        return f"Error: {data['error']}"

    if not data or len(data) == 0:
        return f"No data found for symbol: {symbol}"

    # Extract quote data
    quote = data[0]

    # Format response
    result = f"""Stock Quote: {quote.get('name', 'N/A')} ({symbol})

Current Price: ${quote.get('price', 0):.2f}
Change: ${quote.get('change', 0):.2f} ({quote.get('changesPercentage', 0):.2f}%)
Volume: {quote.get('volume', 0):,}
Market Cap: ${quote.get('marketCap', 0):,}
P/E Ratio: {quote.get('pe', 'N/A')}
Previous Close: ${quote.get('previousClose', 0):.2f}
Day Range: ${quote.get('dayLow', 0):.2f} - ${quote.get('dayHigh', 0):.2f}
"""

    return result


@mcp.tool()
def get_company_profile(symbol: str) -> str:
    """
    Get company profile information for a given symbol

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)

    Returns:
        Formatted string with company profile information
    """
    symbol = symbol.upper().strip()

    # Make API request
    data = make_fmp_request(f"profile/{symbol}")

    # Handle errors
    if "error" in data:
        return f"Error: {data['error']}"

    if not data or len(data) == 0:
        return f"No profile found for symbol: {symbol}"

    # Extract profile data
    profile = data[0]

    # Format response
    result = f"""Company Profile: {profile.get('companyName', 'N/A')} ({symbol})

Industry: {profile.get('industry', 'N/A')}
Sector: {profile.get('sector', 'N/A')}
Country: {profile.get('country', 'N/A')}
Market Cap: ${profile.get('mktCap', 0):,}
Employees: {profile.get('fullTimeEmployees', 'N/A'):,}
Website: {profile.get('website', 'N/A')}
CEO: {profile.get('ceo', 'N/A')}

Description:
{profile.get('description', 'No description available')[:500]}...

Stock Info:
Exchange: {profile.get('exchangeShortName', 'N/A')}
Current Price: ${profile.get('price', 0):.2f}
Beta: {profile.get('beta', 'N/A')}
"""

    return result


def main():
    """Main function to run the server"""
    print("Starting Financial Modeling Prep MCP Server...")

    # Check if API key is set
    if not API_KEY:
        print("Warning: FMP_API_KEY environment variable not set!")
        print("Please set your API key: export FMP_API_KEY='your_api_key_here'")
    else:
        print("API key found, server ready!")

    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()