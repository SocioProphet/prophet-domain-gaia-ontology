.PHONY: validate validate-world-signals

validate: validate-world-signals

validate-world-signals:
	python3 tools/validate_world_signals.py
