# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class AdapterQuery(BaseModel):
    adapterName: str

class CableQuery(BaseModel):
    adapterName: str

class OSRequirementsQuery(BaseModel):
    adapterName: str

class DistanceQuery(BaseModel):
    linkSpeed: str
    cableType: str

@app.post("/get-adapter-overview")
async def get_adapter_overview(query: AdapterQuery):
    return {"overview": f"Overview of {query.adapterName}. (Mocked response)"}

@app.post("/get-adapter-specs")
async def get_adapter_specs(query: AdapterQuery):
    return {"specs": f"Specifications for {query.adapterName}. (Mocked response)"}

@app.post("/get-adapter-cables")
async def get_adapter_cables(query: CableQuery):
    return {"cables": f"Supported cables for {query.adapterName}. (Mocked response)"}

@app.post("/get-os-requirements")
async def get_os_requirements(query: OSRequirementsQuery):
    return {"requirements": f"OS requirements for {query.adapterName}. (Mocked response)"}

@app.post("/get-transceiver-distances")
async def get_transceiver_distances(query: DistanceQuery):
    return {"distance": f"Distance supported for {query.linkSpeed} over {query.cableType}. (Mocked response)"}
