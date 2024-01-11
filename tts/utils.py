import asyncio
import io
import sys
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import edge_tts
import openai
import logging

from gtts import gTTS
from openai import OpenAI
from typing_extensions import Literal

from tts import file_util
from tts.audio_util import mp3_to_wav
from tts.interface import TTS, TTSConfig, AudioWav

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [File \"%(pathname)s\", line %(lineno)d] %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout
    # filename='app.log',
    # filemode='w'
)
