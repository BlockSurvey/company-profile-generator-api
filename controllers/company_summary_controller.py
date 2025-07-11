import requests
import os

API_KEY = os.getenv("PPLX_API_KEY")
BASE_URL = "https://api.perplexity.ai/chat/completions"


class CompanySummaryController:
    def __init__(self):
        pass

    def summarize_company(self, company_name: str) -> str:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "sonar-pro", # sonar
            "messages": [
                {
                    "role": "system",
                    "content": "You are a research assistant that summarizes companies using latest information from the web."
                },
                {
                    "role": "user",
                    "content": f"Summarize {company_name} company. Include: What company does, key message. It is quick summary, no more than 100 words. Don't include references, just the summary."
                }
            ]
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None


    def get_company_summary(self, company_name: str):
        return self.summarize_company(company_name)