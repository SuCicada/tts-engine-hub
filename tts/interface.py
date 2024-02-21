from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Union


@dataclass
class TTSConfig:
    # tts_engine: str
    text: str
    language: str
    speed: float

    @staticmethod
    def from_dict( _config: dict):
        return TTSConfig(**{k: v for k, v in _config.items() if k in TTSConfig.__annotations__})


@dataclass
class AudioWav:
    sampling_rate: int
    wav_bytes: bytes


class TTS(ABC):
    # @staticmethod
    # def get_tts(tts_engine: str):
    #     if tts_engine == "gtts":
    #         from tts.Gtts import GoogleTTS
    #         return GoogleTTS()
    #     elif tts_engine == "edge-tts":
    #         from tts.EdgeTTS import EdgeTTS
    #         return EdgeTTS()
    #     else:
    #         raise Exception("tts_engine not support")

    # @abstractmethod
    def get_stream(self, config: TTSConfig):
        pass

    @abstractmethod
    def get_wav(self, config: Union[TTSConfig, dict]) -> AudioWav:
        pass
