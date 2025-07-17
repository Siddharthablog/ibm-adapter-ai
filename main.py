from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import re

app = FastAPI()

class TextInput(BaseModel):
    text: str  # Required, just like in check-style

class AdapterDetail(BaseModel):
    feature_code: str
    adapter_name: str
    description: str

class Output(BaseModel):
    original_text: str
    matches: List[AdapterDetail]

@app.post("/search-adapter", response_model=Output)
async def search_adapter(input_text: TextInput):
    text = input_text.text.strip()
    matches = []

    # Example regex pattern to extract adapter info (simplified)
    adapter_pattern = re.compile(
        r"Feature Code[:\s]+(?P<feature>\w+)\s+Adapter Name[:\s]+(?P<name>.+?)\s+Description[:\s]+(?P<desc>.*?)(?=\nFeature Code|\Z)",
        re.DOTALL
    )

    for match in adapter_pattern.finditer(text):
        feature = match.group("feature").strip()
        name = match.group("name").strip()
        desc = match.group("desc").strip()

        matches.append(AdapterDetail(
            feature_code=feature,
            adapter_name=name,
            description=desc
        ))

    return {"original_text": text, "matches": matches}
