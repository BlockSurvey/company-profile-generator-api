import requests

def get_stock_symbol_by_name(company_name, api_key):
    url = f"https://financialmodelingprep.com/api/v3/search"
    params = {
        "query": company_name,
        "limit": 10,
        "exchange": "NASDAQ",  # You can also try "NYSE", "AMEX", or remove for all
        "apikey": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()
        if results:
            return results  # List of matching companies with symbols
        else:
            return {"error": "No results found."}
    else:
        return {"error": f"Failed to fetch data: {response.status_code}"}

# Example usage:
api_key = "G8p4HTsqv6y47BPVNMVy1f5CVdqJOQ9Z"  # Replace with your actual FMP API key
company_name = "apple"
symbols = get_stock_symbol_by_name(company_name, api_key)

print(symbols)
