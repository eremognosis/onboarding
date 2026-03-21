
PYTHON = .venv/bin/python
PIP = .venv/bin/pip

.PHONY: help install clean-data run-api all clean-sys

help:
	@echo "AdaptIQ Build System"
	@echo "--------------------"
	@echo "install      : Setup virtual environment and dependencies"
	@echo "clean-data   : Transform raw O*NET Excel/CSVs into ./cleaneddata"
	@echo "run-api      : Fire up the real Flask API (AI/server.py)"
	@echo "all          : Full sequence (Install -> Clean -> Run)"
	@echo "clean-sys    : Nuke __pycache__ and temp files"

# 1. Start from Requirements
install:
	@echo "[!] Building the environment..."
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# 2. Data Cleaning Logic (Bridging raw O*NET to your processed logic)
clean-data:
	@echo "[!] Scrubbing the federal datasets..."
	$(PYTHON) Data/clean.py

# 3. The Real API Endpoint
run-api:
	@echo "[!] Waking up Mistral & Flask..."
	# We use the Flask server inside the AI directory
	$(PYTHON) AI/server.py

# The "I just cloned this and want it to work" command
all: install clean-data run-api

# Housekeeping
clean-sys:
	@echo "[!] Cleaning up the mess..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache