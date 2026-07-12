SHELL := /bin/bash
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

DOCKER_COMPOSE := docker-compose
DOCKER := docker
WEB_CONTAINER := rsvr-sdd-web-1

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  up       Start services in background"
	@echo "  stop     Stop services"
	@echo "  restart  Restart services"
	@echo "  prune    Stop services and prune Docker resources"
	@echo "  weblog   Tail web container logs"
	@echo "  build    Build web image without cache"

.PHONY: stop
stop:
	$(DOCKER_COMPOSE) stop

.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d

.PHONY: restart
restart: stop up

.PHONY: prune
prune: stop
	$(DOCKER) container prune -f
	$(DOCKER) image prune -f
	$(DOCKER) volume prune -f

.PHONY: weblog
weblog:
	$(DOCKER) logs $(WEB_CONTAINER)

.PHONY: build
build:
	$(DOCKER_COMPOSE) build --no-cache

