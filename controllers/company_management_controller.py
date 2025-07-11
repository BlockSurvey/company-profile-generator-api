import os
from typing import List

import requests
from pydantic import BaseModel, Field

API_KEY = os.getenv("PPLX_API_KEY")
BASE_URL = "https://api.perplexity.ai/chat/completions"

class Executive(BaseModel):
    name: str
    title: str
    since: str = Field(None, description="Date they joined the position, if known")

class ExecList(BaseModel):
    company: str
    top_management: List[Executive]

class CompanyManagementController:
    def __init__(self):
        pass

    def fetch_management(self, company_name: str) -> ExecList:
        # JSON schema for structured output
        schema = ExecList.model_json_schema()
        prompt = (
            f"List the top management (C-suite & board leaders) of {company_name}. "
            "For each, provide name, title, and approximate start date. "
            "Respond strictly in JSON following the given schema."
        )

        payload = {
            "model": "sonar-pro",
            "messages": [
                {"role": "system", "content": "You are a structured data assistant."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {"schema": schema}
            },
            "max_tokens": 800,
            "temperature": 0.0
        }

        resp = requests.post(BASE_URL, json=payload,
                            headers={"Authorization": f"Bearer {API_KEY}"})
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return ExecList.model_validate_json(content)

    def get_company_management(self, company_name: str):
        return self.fetch_management(company_name)