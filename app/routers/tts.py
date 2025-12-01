from fastapi import APIRouter, HTTPException
from openai import OpenAI
import base64
import os

router = APIRouter(prefix="/tts", tags=["tts"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/")
async def text_to_speech(payload: dict):
    try:
        text = payload.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="Missing text")

        # Llamada TTS → devuelve HttpxBinaryResponseContent
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            input=text,
            voice="verse",
            response_format="mp3",
        )

        # EXTRAER BYTES CORRECTAMENTE
        audio_bytes = response.read()   # 🔥 ESTE ES EL PUNTO CLAVE

        # Convertir a base64
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        return {"audio_base64": audio_b64}

    except Exception as e:
        print("ERROR TTS:", e)
        raise HTTPException(status_code=500, detail=str(e))
