import requests
from pydantic import BaseModel, Field

# Replace with your actual Perplexity API key
API_KEY = ""
BASE_URL = "https://api.perplexity.ai/chat/completions"

class CompanyOverviewCitations(BaseModel):
    citation_1: str = Field(alias="1", description="Source link for the first citation")
    citation_2: str = Field(alias="2", description="Source link for the second citation")

class CompanyOverview(BaseModel):
    overview: str = Field(description="Overview of the company, General business description (what the company does) Key service offerings Growth drivers (e.g., market expansion, margin acceleration) Strategic focus areas (short, medium, long term) Capital allocation strategies. Apply text formatting.")
    citations: CompanyOverviewCitations

def summarize_company(company_name: str) -> str:

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
        return result["choices"][0]["message"]["content"]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage
if __name__ == "__main__":
    company = "Tesla"
    summary = summarize_company(company)
    if summary:
        print(f"\n📝 Summary for {company}:\n{summary}")
