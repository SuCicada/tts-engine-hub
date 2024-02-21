import base64
import json
import logging
import os
import sys
import tempfile
import unittest
from pathlib import Path

from tts.interface import TTSConfig, AudioWav

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from dotenv import load_dotenv
load_dotenv("../.env")
from server import TTS_ENGINES
from tts import audio_util, file_util


class TestAddition(unittest.TestCase):
    def test_tts_gtts(self):
        engine = TTS_ENGINES["gtts"]
        jj = {"text":
                  "十にん",
              "language": "ja", "speed": 1}
        res = engine.get_wav(jj)
        audio_util.play(res)
        Path("test.wav").write_bytes(res.wav_bytes)

    def test_tts_edge(self):
        engine = TTS_ENGINES["edge-tts"]
        jj = {"text": "こんにちは", "language": "ja", "speed": 1}
        res = engine.get_wav(jj)
        audio_util.play(res)

    def test_tts_openai(self):
        engine = TTS_ENGINES["openai-tts"]
        # for voice in ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]:
        voice = "echo"
        jj = {"text":
                  "終わりに、兄弟たち、わたしたちのために祈ってください。主の言葉が、あなたがたのところでそうであったように、速やかに宣べ伝えられ、あがめられるように、",
              "language": "ja",
              "speed": 1,
              "voice": voice}
        res = engine.get_wav(jj)
        audio_util.play(res)

    def test_tts_lain(self):
        engine = TTS_ENGINES["lain_style_bert_vits2"]
        # for voice in ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]:
        # voice = "echo"
        jj = {"text":
                  "終わりに、兄弟たち、わたしたちのために祈ってください。主の言葉が、あなたがたのところでそうであったように、速やかに宣べ伝えられ、あがめられるように、",
              "language": "ja",
              "speed": 1,
              # "voice": voice
              }
        res = engine.get_wav(jj)
        audio_util.play(res)

    def test(self):
        print("test")
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger("SomeTest.testSomething").setLevel(logging.DEBUG)
        log = logging.getLogger("SomeTest.testSomething")
        log.debug("this= %r", self)

    def test_api(self):
        import requests
        url = "http://localhost:17862/ttsapi/generate_audio"
        req_json = {
            "tts_engine": "edge-tts",
            "text":
                "終わりに、兄弟たち、わたしたちのために祈ってください。主の言葉が、あなたがたのところでそうであったように、速やかに宣べ伝えられ、あがめられるように、",
            "language": "ja", "speed": 1
        }
        response = requests.post(url, json=req_json)
        res = response.json()
        audio = base64.b64decode(res['audio'])
        sampling_rate = res['sampling_rate']
        audio_util.play(AudioWav(sampling_rate, audio))

def test_tts_openai():
    engine = TTS_ENGINES["openai-tts"]
    # for voice in ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]:
    voice = "onyx"
    jj = {"text":
              """
              "你好！最近过得怎么样？有什么新鲜事吗？
              """,
          "language": "ja", "speed": 1, "voice": voice}
    res = engine.get_wav(jj)
    Path("out.wav").write_bytes(res.wav_bytes)
    audio_util.play(res)

if __name__ == "__main__":
    unittest.main()
