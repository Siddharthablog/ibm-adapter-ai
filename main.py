from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Manually loaded or pre-converted PDF text (replace with actual content)
with open("adapter-spec.txt", "r", encoding="utf-8") as f:
    pdf_text = f.read()

class AdapterQuery(BaseModel):
    adapterName: str

class CableQuery(BaseModel):
    adapterName: str

class OSRequirementsQuery(BaseModel):
    adapterName: str

class DistanceQuery(BaseModel):
    linkSpeed: str
    cableType: str

def find_lines_containing(keyword: str, limit=5) -> List[str]:
    lines = pdf_text.splitlines()
    matches = [line.strip() for line in lines if keyword.lower() in line.lower()]
    return matches[:limit] if matches else ["No relevant data found."]

@app.post("/get-adapter-overview")
async def get_adapter_overview(query: AdapterQuery):
    results = find_lines_containing(query.adapterName)
    return {
        "adapter": query.adapterName,
        "overview": results
    }

@app.post("/get-adapter-specs")
async def get_adapter_specs(query: AdapterQuery):
    keyword = f"{query.adapterName} specifications"
    results = find_lines_containing(keyword)
    return {
        "adapter": query.adapterName,
        "specifications": results
    }

@app.post("/get-adapter-cables")
async def get_adapter_cables(query: CableQuery):
    keyword = f"{query.adapterName} cable"
    results = find_lines_containing(keyword)
    return {
        "adapter": query.adapterName,
        "supported_cables": results
    }

@app.post("/get-os-requirements")
async def get_os_requirements(query: OSRequirementsQuery):
    keyword = f"{query.adapterName} os requirements"
    results = find_lines_containing(keyword)
    return {
        "adapter": query.adapterName,
        "os_requirements": results
    }

@app.post("/get-transceiver-distances")
async def get_transceiver_distances(query: DistanceQuery):
    keyword = f"{query.linkSpeed} {query.cableType}"
    results = find_lines_containing(keyword)
    return {
        "search_phrase": keyword,
        "distance_info": results
    }
