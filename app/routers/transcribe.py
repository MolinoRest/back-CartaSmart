from fastapi import APIRouter, UploadFile, File, HTTPException
from openai import OpenAI
import os

router = APIRouter(prefix="/transcribe", tags=["transcription"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()

        response = client.audio.transcriptions.create(
            file=(file.filename or "audio.webm", audio_bytes, file.content_type),
            model="gpt-4o-transcribe",
        )

        return {"text": response.text}

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
