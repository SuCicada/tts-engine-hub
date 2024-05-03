```bash
brew install libsodium
```

# run
```bash
dokcker run -d -p 41402:41402 --name tts-engine-hub \
		--env-file .env \
		sucicada/tts-engine-hub:latest
```
选择python的原因：
因为语音处理的代码是直接从之前给 so-vits-svc 写的代码搬过来的
