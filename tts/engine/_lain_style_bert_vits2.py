import logging
import os
from io import BytesIO

import requests
from gtts import gTTS

from tts import audio_util
from tts.audio_util import mp3_to_wav
from tts.interface import TTS, TTSConfig, AudioWav

logger = logging.getLogger('tts.engine.google')


class LainStyleBertVits2TTS(TTS):
    language_dict = {
        "ja": "JP",
        # "en": "en",
        # "zh": "zh-CN"
    }

    def get_wav(self, _config: dict) -> AudioWav:
        # config = TTSConfig(**{k: v for k, v in _config.items() if k in TTSConfig.__annotations__})
        config = TTSConfig.from_dict(_config)
        logger.info(f"LainTTS: {config}")

        lang = self.language_dict[config.language]

        url = os.environ["STYLE_BERT_VITS2_API"]
        req_json = {
            # "tts_engine": "gtts",
            "text": config.text,
            "language": lang,
            "length": config.speed,
            # "voice": "alloy"
        }
        response = requests.post(url, json=req_json)
        wav_bytes = response.content
        sampling_rate = audio_util.get_sampling_rate_from_wab_bytes(wav_bytes)
        # res = response.json()
        # audio_base64 = res['audio']
        # audio = base64.b64decode(audio_base64)
        # sampling_rate = res['sampling_rate']
        # origin_audio = AudioWav(sampling_rate, audio)
        # print("origin_audio over")
        # audio_util.play(audio)

        return AudioWav(sampling_rate, wav_bytes)
        # return stream
