NAME		:= local/snitch
TAG    		:= $(shell git log -1 --pretty=%h)
DOCKERFILE 	:= ./Dockerfile
PORT		:= 8000

build:
	docker build -t ${NAME}:${TAG} -t ${NAME}:latest -f ${DOCKERFILE} .

run:
	docker run -p ${PORT}:${PORT} -t ${NAME}:${TAG}

debug:
	docker run -v $(shell pwd):/api -p ${PORT}:${PORT} -e LOG_LEVEL=debug -t ${NAME}:${TAG}

stop:
	docker stop $(shell docker ps -qa) && docker rm $(shell docker ps -qa)

test:
	docker run -v $(shell pwd):/api -t ${NAME}:${TAG} bash -c "python -m unittest discover tests"

.PHONY: build run debug stop test
