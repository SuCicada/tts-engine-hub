ifneq ("$(wildcard .env)","")
	include .env
	export
endif

run:
	python server.py
install:
	apt update && apt install -y libsndfile1 ffmpeg
	pip install -r requirements.txt


remote_docker := unset DOCKER_HOST; docker
ifeq ($(REMOTE),true)
	remote_docker := DOCKER_HOST=$(REMOTE_DOCKER_HOST) docker
endif

service_name = tts-engine-hub

docker-build:
	$(remote_docker) build -t sucicada/$(service_name):latest .

docker-push:
	docker push sucicada/$(service_name):latest

_docker-run: docker-build
	@echo $(remote)
	@echo $(DOCKER_HOST)
	@echo $(remote_docker)
	$(remote_docker) stop $(service_name) || true
	$(remote_docker) rm $(service_name) || true
	$(remote_docker) run -d -p 41402:41402 --name $(service_name) \
		--env-file .env \
		--restart=always \
		sucicada/$(service_name):latest

docker-run-remote:
	REMOTE=true make _docker-run

docker-run-local:
	make _docker-run

