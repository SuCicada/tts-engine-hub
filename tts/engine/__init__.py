from tts.interface import TTS

from ._google import GoogleTTS
from ._edge import EdgeTTS
from ._openai import OpenAITTS
from ._lain_style_bert_vits2 import LainStyleBertVits2TTS

TTS_ENGINES: dict[str:TTS] = {
    "gtts": GoogleTTS(),
    "edge-tts": EdgeTTS(),
    "openai-tts": OpenAITTS(),
    "lain_style_bert_vits2": LainStyleBertVits2TTS(),
}