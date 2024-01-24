import argparse
import asyncio
import base64
import os
from dataclasses import dataclass

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from tts.engine import EdgeTTS, GoogleTTS, OpenAITTS
from tts.interface import TTS

# Define an enumeration class
# class TTS_ENGINE(Enum):
#     gtts = GoogleTTS()
# GREEN = 2
# BLUE = 3
from dotenv import load_dotenv
load_dotenv()

TTS_ENGINES: dict[str:TTS] = {
    "gtts": GoogleTTS(),
    "edge-tts": EdgeTTS(),
    "openai-tts": OpenAITTS()
}

app = FastAPI()
# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @dataclass
# class TTSRequest:
#     text: str
#     language: str
#     speed: float

@app.post("/ttsapi/generate_audio")
async def generate_audio(request: Request):
    params = await request.json()
    tts_engine: str = params.pop("tts_engine")
    engine: TTS = TTS_ENGINES[tts_engine]
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None,
                                     lambda: engine.get_wav(params))
    audio = base64.b64encode(res.wav_bytes).decode("utf-8")
    return {
        "sampling_rate": res.sampling_rate,
        "audio": audio,
    }


def main():
    # POST /ttsapi/generate_audio -> edge-tts
    # -> call engine.say: com.linkedin.edge.Engine
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help='port')
    args = parser.parse_args()
    port = args.port
    if not port:
        port = os.environ.get('PORT', 41402)
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)


if __name__ == '__main__':
    main()
