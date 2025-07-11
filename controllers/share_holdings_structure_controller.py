import os
import requests
import pandas as pd

API_KEY = os.getenv("FMP_API_KEY", "<YOUR_KEY>")
BASE_URL = "https://financialmodelingprep.com/api/v3"

class ShareHoldingsStructureController:
    def __init__(self):
        pass

    def get_pie_data(self, data: dict) -> dict:
        # Prepare Business Pie Chart JSON
        business_entry = data["business"][0]["data"]
        business_pie = {
            "type": "pie",
            "data": {
                "labels": list(business_entry.keys()),
                "datasets": [
                    {
                        "data": list(business_entry.values()),
                        "backgroundColor": [
                            "#FF6384", "#36A2EB", "#FFCE56"
                        ]
                    }
                ]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "legend": {"position": "right"},
                    "title": {"display": True, "text": "Tesla Revenue by Business Segment (2024)"}
                }
            }
        }

        # Prepare Region Pie Chart JSON
        region_entry = data["region"][0]["data"]
        region_pie = {
            "type": "pie",
            "data": {
                "labels": list(region_entry.keys()),
                "datasets": [
                    {
                        "data": list(region_entry.values()),
                        "backgroundColor": [
                            "#4BC0C0", "#9966FF", "#FF9F40"
                        ]
                    }
                ]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "legend": {"position": "right"},
                    "title": {"display": True, "text": "Tesla Revenue by Region (2024)"}
                }
            }
        }

        return {"business": business_pie, "region": region_pie}

    def fetch_and_build_pie(self, symbol: str, api_key: str) -> dict:
        """
        Fetch revenue segmentation data via free FMP endpoints and build Chart.js pie configs.
        Returns dict with raw data and correctly populated pie chart JSON.
        """
        base = "https://financialmodelingprep.com/stable"
        biz_resp = requests.get(f"{base}/revenue-product-segmentation",
                                params={"symbol": symbol, "apikey": api_key})
        biz_resp.raise_for_status()
        business_data = biz_resp.json()  # :contentReference[oaicite:1]{index=1}

        geo_resp = requests.get(f"{base}/revenue-geographic-segmentation",
                                params={"symbol": symbol, "apikey": api_key})
        geo_resp.raise_for_status()
        region_data = geo_resp.json()    # :contentReference[oaicite:2]{index=2}

        return self.get_pie_data({"business": business_data, "region": region_data})

    def get_share_holdings_structure(self, symbol: str):
        return self.fetch_and_build_pie(symbol, API_KEY)