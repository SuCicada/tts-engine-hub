import asyncio
import io
import logging
import edge_tts
from tts.audio_util import mp3_to_wav
from tts.interface import TTS, TTSConfig, AudioWav

logger = logging.getLogger('tts.engine.google')

class EdgeTTS(TTS):
    language_dict = {
        "ja": "ja-JP-NanamiNeural",
        "en": "en-US-AriaNeural",
        "zh": "zh-CN-XiaoxiaoNeural"
    }

    def get_wav(self, _config: dict) -> AudioWav:
        config = TTSConfig(**{k: v for k, v in _config.items() if k in TTSConfig.__annotations__})
        logger.info(f"EdgeTTS: {config}")
        voice = self.language_dict[config.language]
        _rate = config.speed
        _rate = f"+{int((_rate - 1) * 100)}%" if _rate >= 1 else f"{int((1 - _rate) * 100)}%"

        async def _write():
            file_in_memory = io.BytesIO()
            communicate = edge_tts.Communicate(config.text, voice, rate=_rate)
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file_in_memory.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    print(f"WordBoundary: {chunk}")
            return file_in_memory

        stream = asyncio.run(_write())
        mp3_bytes = stream.getvalue()
        sampling_rate, wav_bytes = mp3_to_wav(mp3_bytes)
        return AudioWav(sampling_rate, wav_bytes)
