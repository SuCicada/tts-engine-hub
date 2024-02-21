import base64
import os
import sys
from pathlib import Path

import requests

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from tts import audio_util
from tts.interface import AudioWav




def test_api():
    url = "http://asus.sucicada.me:41402/ttsapi/generate_audio"
    req_json = {
        "tts_engine": "gtts",
        # "tts_engine": "openai-tts",
        "text":
            """
              どんなことでも、思い煩うのはやめなさい。何事につけ、感謝を込めて祈りと願いをささげ、求めているものを神に打ち明けなさい。 
そうすれば、あらゆる人知を超える神の平和が、あなたがたの心と考えとをキリスト・イエスによって守るでしょう。
            """,
        "language": "ja",
        "speed": 1,
        "voice": "alloy"
    }
    response = requests.post(url, json=req_json)
    res = response.json()
    audio_base64 = res['audio']
    audio = base64.b64decode(audio_base64)
    sampling_rate = res['sampling_rate']
    origin_audio = AudioWav(sampling_rate, audio)
    print("origin_audio over")
    audio_util.play(origin_audio)

def test_api_all():
    import requests
    url = "http://asus.sucicada.me:41402/ttsapi/generate_audio"
    req_json = {
        "tts_engine": "gtts",
        # "tts_engine": "openai-tts",
        "text":
            """
             愛する人たち、あなたがたに勧めます。いわば旅人であり、仮住まいの身なのですから、魂に戦いを挑む肉の欲を避けなさい。
            """,
        "language": "ja",
        "speed": 1,
        "voice": "alloy"
    }
    response = requests.post(url, json=req_json)
    res = response.json()
    audio_base64 = res['audio']
    audio = base64.b64decode(audio_base64)
    sampling_rate = res['sampling_rate']
    origin_audio = AudioWav(sampling_rate, audio)
    print("origin_audio over")

    req_json = {
        "audio": audio_base64,
        "auto_predict_f0":True,
        "cluster_ratio": 0,
        # "tran":3
    }
    url = 'http://asus.sucicada.me:17861/svcapi/audio_to_audio'
    response = requests.post(url, json=req_json)
    res = response.json()
    audio = base64.b64decode(res['audio'])
    sampling_rate = res['sampling_rate']
    target_audio = AudioWav(sampling_rate, audio)
    print("target_audio over")

    # audio_util.play(origin_audio)
    audio_util.play(target_audio)
    Path("origin.wav").write_bytes(origin_audio.wav_bytes)
    Path("lain.wav").write_bytes(target_audio.wav_bytes)


if __name__ == '__main__':
    # test_tts_openai()
    # test_api()
    test_api_all()
