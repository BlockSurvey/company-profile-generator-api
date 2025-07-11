import os

import pandas as pd
import requests

API_KEY = os.getenv("FMP_API_KEY", "<YOUR_KEY>")
BASE_URL = "https://financialmodelingprep.com/api/v3"

class CompanyStockDetailsController:
    def __init__(self):
        pass

    def get_stock_symbol_by_name(self, company_name):
        url = f"{BASE_URL}/search"
        params = {
            "query": company_name,
            "limit": 10,
            "exchange": "NASDAQ",  # You can also try "NYSE", "AMEX", or remove for all
            "apikey": API_KEY
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            results = response.json()

            if results and len(results) > 0:
                # Return the first result
                return results[0]
            else:
                return {"error": "No results found."}
        else:
            return {"error": f"Failed to fetch data: {response.status_code}"}


    def get_company_stock_details(self, company_name: str):
        return self.get_stock_symbol_by_name(company_name)