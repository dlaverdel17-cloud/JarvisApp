from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os

app = FastAPI(title="Jarvis AI Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API KEY DE GEMINI DESDE RENDER
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Cliente de Gemini
client = genai.Client(api_key=GEMINI_API_KEY)


class QueryModel(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {
        "status": "JARVIS System Online"
    }


@app.post("/api/jarvis")
async def process_jarvis(query: QueryModel):
    try:

        print("PREGUNTA RECIBIDA:", query.prompt)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query.prompt
        )

        print("RESPUESTA:", response.text)

        return {
            "reply": response.text
        }

    except Exception as e:

        print("ERROR DETALLADO:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
