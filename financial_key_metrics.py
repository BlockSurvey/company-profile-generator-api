import requests
import os

API_KEY = os.getenv("FMP_API_KEY", "<YOUR_KEY>")
BASE_URL = "https://financialmodelingprep.com/api/v3"

def fetch_data(endpoint: str) -> list:
    # Fix URL construction to handle & vs ? correctly
    url = f"{BASE_URL}/{endpoint}&apikey={API_KEY}" if "?" in endpoint else f"{BASE_URL}/{endpoint}?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {endpoint}: {response.status_code}")
        return []
    data = response.json()
    return data if isinstance(data, list) else []

def format_percent(value):
    if value is None:
        return None
    return f"{round(value * 100, 1)}%"

def get_financial_metrics(symbol: str):
    # Get last 3 years historical data
    income_data = fetch_data(f"income-statement/{symbol}?limit=3")
    ratio_data = fetch_data(f"ratios/{symbol}?limit=3")
    
    # Get current and next 2 years forecast data
    forecast_data = fetch_data(f"forecast/income-statement/{symbol}?limit=3")
    analyst_estimates = fetch_data(f"analyst-estimates/{symbol}?period=annual&limit=3")

    result = []

    # Historical (Last 3 years)
    for i in range(len(income_data)):
        year = income_data[i].get("calendarYear")
        result.append({
            "year": year,
            "type": "Actual",
            "revenue": income_data[i].get("revenue", 0) // 1_000_000,
            "ebitda": income_data[i].get("ebitda", 0) // 1_000_000,
            "eps": round(income_data[i].get("eps", 0), 2),
            "netIncome": income_data[i].get("netIncome", 0) // 1_000_000,
            "ebitdaMargin": format_percent(ratio_data[i].get("ebitdaMargin") if i < len(ratio_data) else None),
            "roe": format_percent(ratio_data[i].get("returnOnEquity") if i < len(ratio_data) else None)
        })

    # Company Forecast (Current + 2 years)
    for item in forecast_data:
        year = item.get("calendarYear")
        result.append({
            "year": year,
            "type": "Forecast (Company)",
            "revenue": item.get("revenue", 0) // 1_000_000,
            "ebitda": item.get("ebitda", 0) // 1_000_000,
            "eps": round(item.get("eps", 0), 2),
            "netIncome": item.get("netIncome", 0) // 1_000_000,
            "ebitdaMargin": None,
            "roe": None
        })

    # Analyst Estimates (Current + 2 years)
    for item in analyst_estimates:
        year = item.get("date")
        result.append({
            "year": year,
            "type": "Forecast (Analyst)",
            "revenue": item.get("estimatedRevenueAvg", 0) // 1_000_000,
            "ebitda": item.get("estimatedEbitdaAvg", 0) // 1_000_000,
            "eps": round(item.get("estimatedEpsAvg", 0), 2),
            "netIncome": item.get("estimatedNetIncomeAvg", 0) // 1_000_000,
            "ebitdaMargin": None,
            "roe": None
        })

    return result


if __name__ == "__main__":
    symbol = "AAPL"  # Replace with any public company symbol
    data = get_financial_metrics(symbol)

    import json
    print(json.dumps(data, indent=2))
