from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

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
    return {
        "question": f"What does the adapter {query.adapterName} do?"
    }

@app.post("/get-adapter-specs")
async def get_adapter_specs(query: AdapterQuery):
    return {
        "question": f"Give me the specifications of adapter {query.adapterName}."
    }

@app.post("/get-adapter-cables")
async def get_adapter_cables(query: CableQuery):
    return {
        "question": f"What cables are supported by adapter {query.adapterName}?"
    }

@app.post("/get-os-requirements")
async def get_os_requirements(query: OSRequirementsQuery):
    return {
        "question": f"Which operating systems are compatible with adapter {query.adapterName}?"
    }

@app.post("/get-transceiver-distances")
async def get_transceiver_distances(query: DistanceQuery):
    return {
        "question": (
            f"What is the maximum supported distance for {query.linkSpeed} "
            f"over {query.cableType} cable?"
        )
    }
