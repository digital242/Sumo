# Sumo — common tasks. Run `make help` for the list.

PY ?= python3

.DEFAULT_GOAL := help

.PHONY: help install dev test doctor chat run morning skills agents clean

help: ## Show this help
	@echo "Sumo — make targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install: ## Install the `sumo` command (editable)
	$(PY) -m pip install -e .

dev: ## Install with dev extras (pytest)
	$(PY) -m pip install -e ".[dev]"

test: ## Run the offline test suite
	$(PY) -m pytest -q

doctor: ## Show engine/model status
	$(PY) -m sumo.cli doctor

chat: ## Interactive chat REPL
	$(PY) -m sumo.cli chat

run: ## Run an agent, e.g. `make run AGENT=react GOAL="add 2 and 3"`
	$(PY) -m sumo.cli run $(AGENT) $(GOAL) --trace

morning: ## Today's briefing
	$(PY) -m sumo.cli morning

skills: ## List the skill catalog
	$(PY) -m sumo.cli skills

agents: ## List available agents
	$(PY) -m sumo.cli agents

clean: ## Remove build artifacts and caches
	rm -rf build dist *.egg-info .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
