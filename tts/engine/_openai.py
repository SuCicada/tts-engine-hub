import logging
import os
from dataclasses import dataclass
from pathlib import Path

from openai import OpenAI
from typing_extensions import Literal

from tts import file_util
from tts.audio_util import mp3_to_wav
from tts.interface import TTS, TTSConfig, AudioWav

logger = logging.getLogger('tts.engine.google')


@dataclass
class OpenAITTSConfig(TTSConfig):
    voice: Literal[
        "alloy",
        "echo",  # 英语口音
        "fable",
        "onyx",  # 低沉
        "nova",  # 偏向女性
        "shimmer"  # 英语口音严重，不好
    ]


class OpenAITTS(TTS):
    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
    )

    def get_wav(self, _config: dict) -> AudioWav:
        config = OpenAITTSConfig(**{k: v for k, v in _config.items() if
                                    k in {**TTSConfig.__annotations__, **OpenAITTSConfig.__annotations__}})

        logger.info(f"OpenAITTS: {config}")
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=config.voice,
            input=config.text,
            speed=config.speed,
            response_format="mp3",
        )
        with file_util.MyNamedTemporaryFile() as temp_path:
            response.stream_to_file(temp_path)
            mp3_bytes = Path(temp_path).read_bytes()
            sampling_rate, wav_bytes = mp3_to_wav(mp3_bytes)
        return AudioWav(sampling_rate, wav_bytes)
