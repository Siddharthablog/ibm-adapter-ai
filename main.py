from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import re

app = FastAPI()

class TextInput(BaseModel):
    text: str
    adapter_name: Optional[str] = None

class AdapterResponse(BaseModel):
    adapter_name: str
    result: Optional[str]

class CableResponse(BaseModel):
    adapter_name: str
    cables: Optional[List[str]]

def extract_section(text: str, adapter_name: Optional[str]):
    # Match sections like: 01CV450 - Dual Port 10GbE SFP+ Adapter
    pattern = r"(?P<name>[A-Z0-9]{6,})[\s\-–:]+(?P<desc>.+?)(?=(\n[A-Z0-9]{6,}[\s\-–:])|\Z)"
    matches = re.finditer(pattern, text, re.DOTALL)
    results = []

    for match in matches:
        name = match.group("name").strip()
        desc = match.group("desc").strip()
        if not adapter_name or adapter_name.upper() == name:
            results.append((name, desc))

    return results

@app.post("/get-overview", response_model=List[AdapterResponse])
async def get_overview(input_text: TextInput):
    sections = extract_section(input_text.text, input_text.adapter_name)
    return [{"adapter_name": name, "result": desc} for name, desc in sections]

@app.post("/get-speed", response_model=List[AdapterResponse])
async def get_speed(input_text: TextInput):
    sections = extract_section(input_text.text, input_text.adapter_name)
    results = []
    for name, desc in sections:
        speed_match = re.search(r"\b\d+\s?(Gbps|Gb/s|Mbps|Mb/s)\b", desc, re.IGNORECASE)
        results.append({
            "adapter_name": name,
            "result": speed_match.group(0) if speed_match else "Not found"
        })
    return results

@app.post("/get-cables", response_model=List[CableResponse])
async def get_cables(input_text: TextInput):
    cable_keywords = ["DAC", "RJ45", "Fiber", "SFP", "QSFP", "Twinax"]
    sections = extract_section(input_text.text, input_text.adapter_name)
    results = []
    for name, desc in sections:
        cables = list(set([cable for cable in cable_keywords if cable.lower() in desc.lower()]))
        results.append({
            "adapter_name": name,
            "cables": cables if cables else None
        })
    return results

@app.post("/get-os", response_model=List[AdapterResponse])
async def get_os(input_text: TextInput):
    sections = extract_section(input_text.text, input_text.adapter_name)
    results = []
    for name, desc in sections:
        os_match = re.search(r"(Windows|Linux|AIX|RHEL|SUSE|Ubuntu)[^\.\n]*", desc, re.IGNORECASE)
        results.append({
            "adapter_name": name,
            "result": os_match.group(0) if os_match else "Not found"
        })
    return results

@app.post("/get-all-adapter-info")
async def get_all_adapter_info(input_text: TextInput):
    sections = extract_section(input_text.text, input_text.adapter_name)
    combined = []

    for name, desc in sections:
        speed_match = re.search(r"\b\d+\s?(Gbps|Gb/s|Mbps|Mb/s)\b", desc, re.IGNORECASE)
        os_match = re.search(r"(Windows|Linux|AIX|RHEL|SUSE|Ubuntu)[^\.\n]*", desc, re.IGNORECASE)
        cable_keywords = ["DAC", "RJ45", "Fiber", "SFP", "QSFP", "Twinax"]
        cables = list(set([cable for cable in cable_keywords if cable.lower() in desc.lower()]))

        combined.append({
            "adapter_name": name,
            "overview": desc,
            "speed": speed_match.group(0) if speed_match else None,
            "os_support": os_match.group(0) if os_match else None,
            "supported_cables": cables if cables else None
        })

    return {"adapters": combined if combined else "No adapter info found."}
