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
        # "tts_engine": "gtts",
        "tts_engine": "openai-tts",
        "text":
            """
              信仰によって、わたしたちは、この世界が神の言葉によって創造され、従って見えるものは、目に見えているものからできたのではないことが分かるのです。
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
    url = "http://localhost:17862/ttsapi/generate_audio"
    req_json = {
        # "tts_engine": "gtts",
        "tts_engine": "openai-tts",
        "text":
            """
              网络安全是保护计算机系统、网络系统、数据以及网络用户免受未经授权访问、损坏、窃取或意外损失的一系列措施和实践。它涉及保护网络系统免受恶意攻击、网络犯罪行为、未经授权的访问、数据泄露和破坏等各种威胁。
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
        # "auto_predict_f0":False,
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
    test_api()
