import json
import os

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(
    title="VisitorAI",
    description="Ollama ile ziyaretçi ihtiyacını analiz eden örnek AI web uygulaması.",
    version="1.0.0",
)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


class VisitorInput(BaseModel):
    profession: str = Field(min_length=2, max_length=100)
    ai_usage: str = Field(min_length=2, max_length=100)
    technical_level: int = Field(ge=1, le=5)
    expectation: str = Field(min_length=3, max_length=1000)


ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "profile": {"type": "string"},
        "ai_level": {"type": "string"},
        "priority_need": {"type": "string"},
        "use_cases": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
            "maxItems": 5,
        },
        "recommendation": {"type": "string"},
    },
    "required": [
        "profile",
        "ai_level",
        "priority_need",
        "use_cases",
        "recommendation",
    ],
}


@app.get("/")
async def home():
    return FileResponse("static/index.html")


@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            response.raise_for_status()

        return {
            "status": "ok",
            "ollama": "connected",
            "model": MODEL_NAME,
        }
    except Exception as exc:
        return {
            "status": "warning",
            "ollama": "unreachable",
            "model": MODEL_NAME,
            "detail": str(exc),
        }


@app.post("/api/analyze")
async def analyze(visitor: VisitorInput):
    system_prompt = """
Sen bir kullanıcı içgörüsü ve yapay zeka kullanım danışmanısın.
Görevin, kullanıcının verdiği sınırlı cevaplardan yalnızca iş/teknoloji ihtiyaçlarına
yönelik kısa ve faydalı bir profil oluşturmaktır.

Kurallar:
- Hassas kişisel özellikler hakkında çıkarım yapma.
- Sağlık, siyasi görüş, din, etnik köken, cinsel yönelim, finansal durum gibi
  hassas alanlarda tahmin üretme.
- Kullanıcıya kesin kişilik etiketi yapıştırma.
- Sonuçları Türkçe yaz.
- Kısa, profesyonel ve uygulanabilir öneriler üret.
"""

    user_prompt = f"""
Kullanıcı bilgileri:

Meslek / alan: {visitor.profession}
Yapay zekayı kullanım amacı: {visitor.ai_usage}
Teknik seviye (1-5): {visitor.technical_level}
Yapay zekadan beklenti: {visitor.expectation}

Bu kullanıcı için:
1. İş/teknoloji odaklı kısa profil
2. AI kullanım seviyesi
3. Öncelikli ihtiyaç
4. 3-5 uygun kullanım alanı
5. Tek bir kişiselleştirilmiş öneri

oluştur.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "format": ANALYSIS_SCHEMA,
        "options": {
            "temperature": 0.3
        },
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"{OLLAMA_URL}/api/chat", json=payload)
            response.raise_for_status()
            ollama_data = response.json()

        raw_content = ollama_data["message"]["content"]
        result = json.loads(raw_content)
        return result

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Ollama'ya bağlanılamadı. Ollama'nın çalıştığını kontrol et.",
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama API hatası: {exc.response.text}",
        )
    except (KeyError, json.JSONDecodeError):
        raise HTTPException(
            status_code=502,
            detail="Model beklenen JSON formatında cevap vermedi.",
        )


app.mount("/static", StaticFiles(directory="static"), name="static")
