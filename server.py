import argparse
import asyncio
import base64
import os
from dataclasses import dataclass

import uvicorn
# Define an enumeration class
# class TTS_ENGINE(Enum):
#     gtts = GoogleTTS()
# GREEN = 2
# BLUE = 3
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from tts.engine import *
from tts.interface import TTS

load_dotenv()

app = FastAPI(
    title="TTS API",
)
# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @dataclass
class TTSRequest(BaseModel):
    text: str = Field(...)
    # language: str
    tts_engine: str = Field(..., description="""TTS engine, one of <br>
                            %s
                            """ % "<br>".join(TTS_ENGINES.keys()))
    speed: float = Field(1.0, description="Speed of speech")

    class Config:
        extra = "allow"


# @dataclass
class Response(BaseModel):
    sampling_rate: int = Field(..., description="sampling rate")
    audio: str = Field(..., description="audio base64 encoded")


@app.post(
    "/ttsapi/generate_audio",
    description="Generate audio from text",
    #     openapi_extra={
    #     "requestBody": {
    #         "content": {
    #             "application/json": {
    #                 "schema": {
    #                     "type": "object",
    #                     "properties": {
    #                         "text": {
    #                             "type": "string",
    #                             "description": "Text to be synthesized"
    #                         },
    #                     }
    #                 }
    #             }
    #         }
    #     },
    # }
)
async def generate_audio(request: TTSRequest) -> Response:
    params: dict = request.model_dump()
    tts_engine: str = params.pop("tts_engine")
    text: str = params.get("text")
    tts_engine = request.tts_engine
    text = request.text
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    engine: TTS = TTS_ENGINES[tts_engine]
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None, lambda: engine.get_wav(params))
    audio = base64.b64encode(res.wav_bytes).decode("utf-8")
    return Response(
        sampling_rate=res.sampling_rate,
        audio=audio,
    )


# def add_docs_api():
#     @app.get("/openapi.json", include_in_schema=False)
#     async def _():
#         return app.openapi()


#     @app.get("/docs", include_in_schema=False)
#     async def _():
#         return get_swagger_ui_html(openapi_url="/openapi.json", title="API documentation")
# add_docs_api()
def main():
    # POST /ttsapi/generate_audio -> edge-tts
    # -> call engine.say: com.linkedin.edge.Engine
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help="port")
    args = parser.parse_args()
    port = args.port
    if not port:
        port = os.environ.get("PORT", 41402)
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True,
                root_path=os.environ.get("ROOT_PATH", "/tts-hub"),
                )


if __name__ == "__main__":
    main()
