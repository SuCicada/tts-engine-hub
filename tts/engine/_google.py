import logging
from io import BytesIO
from gtts import gTTS
from tts.audio_util import mp3_to_wav
from tts.interface import TTS, TTSConfig, AudioWav

logger = logging.getLogger('tts.engine.google')

class GoogleTTS(TTS):
    language_dict = {
        "ja": "ja",
        "en": "en",
        "zh": "zh-CN"
    }

    def get_wav(self, _config: dict) -> AudioWav:
        config = TTSConfig(**{k: v for k, v in _config.items() if k in TTSConfig.__annotations__})
        logger.info(f"GoogleTTS: {config}")

        lang = self.language_dict[config.language]

        stream = BytesIO()
        tts = gTTS(config.text, lang=lang, slow=False)
        tts.write_to_fp(stream)
        mp3_bytes = stream.getvalue()
        sampling_rate, wav_bytes = mp3_to_wav(mp3_bytes)
        return AudioWav(sampling_rate, wav_bytes)
        # return stream
