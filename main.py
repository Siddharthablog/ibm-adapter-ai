from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import re

app = FastAPI()

class TextInput(BaseModel):
    text: str
    query: Optional[str] = None  # e.g., "01CV450" or "MQ Adapter"

class AdapterDetail(BaseModel):
    feature_code: str
    adapter_name: str
    description: str
    page: Optional[int] = None

class Output(BaseModel):
    query: Optional[str]
    matches: List[AdapterDetail]

@app.post("/search-adapter", response_model=Output)
async def search_adapter(input: TextInput):
    text = input.text
    query = input.query.strip() if input.query else ""

    # Regular expression to extract adapter entries
    adapter_pattern = re.compile(
        r"Feature Code[:\s]+(?P<feature>\w+)\s+Adapter Name[:\s]+(?P<name>.+?)\s+Description[:\s]+(?P<desc>.*?)(?=\nFeature Code|\Z)",
        re.DOTALL
    )

    matches = []
    for match in adapter_pattern.finditer(text):
        feature = match.group("feature").strip()
        name = match.group("name").strip()
        desc = match.group("desc").strip()

        # If user specified a query, filter for it
        if query:
            if query.lower() not in feature.lower() and query.lower() not in name.lower():
                continue

        matches.append(AdapterDetail(
            feature_code=feature,
            adapter_name=name,
            description=desc
        ))

    return {
        "query": query,
        "matches": matches
    }
