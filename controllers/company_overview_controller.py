import requests
from pydantic import BaseModel, Field
import os

API_KEY = os.getenv("PPLX_API_KEY")
BASE_URL = "https://api.perplexity.ai/chat/completions"

class CompanyOverviewCitations(BaseModel):
    citation_1: str = Field(alias="1", description="Source link for the first citation")
    citation_2: str = Field(alias="2", description="Source link for the second citation")

class CompanyOverview(BaseModel):
    overview: str = Field(description="Overview of the company, General business description (what the company does) Key service offerings Growth drivers (e.g., market expansion, margin acceleration) Strategic focus areas (short, medium, long term) Capital allocation strategies. Apply text formatting.")
    citations: CompanyOverviewCitations

class CompanyOverviewController:
    def __init__(self):
        pass

    def get_company_overview(self, company_name: str) -> str:
        schema = CompanyOverview.model_json_schema()

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
                    "content": f"""Company Overview of {company_name}. I need below list of information:
                        General business description (what the company does)
                        Key service offerings
                        Growth drivers (e.g., market expansion, margin acceleration)
                        Strategic focus areas (short, medium, long term)
                        Capital allocation strategies.
                    """
                }
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {"schema": schema}
            }
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            return CompanyOverview.model_validate_json(result["choices"][0]["message"]["content"])
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
