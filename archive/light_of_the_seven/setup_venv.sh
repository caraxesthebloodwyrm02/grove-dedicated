#!/bin/bash

# setup_venv.sh
# Optimized setup for existing .venv and Ollama

echo "========================================"
echo " GRID RAG Environment Setup"
echo "========================================"

# 1. Check .venv exists
echo ""
echo "[1/3] Checking Virtual Environment..."
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment '.venv' not found."
    exit 1
fi

# 2. Activate venv and Install Python Dependencies
echo "[2/3] Activating .venv and installing/upgrading packages..."

# Activate
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi

# Install packages
echo "Installing: chromadb, httpx, numpy, ollama"
pip install --upgrade chromadb httpx numpy ollama

if [ $? -eq 0 ]; then
    echo "Python dependencies installed successfully."
else
    echo "Error: Failed to install Python packages."
    exit 1
fi

# 3. Check and Pull Ollama Models
echo ""
echo "[3/3] Checking Ollama models..."

# Check if ollama command works (service running)
if ! ollama list > /dev/null 2>&1; then
    echo "Warning: Could not connect to Ollama. Please ensure it is running (run 'ollama serve')."
    echo "Skipping model pull..."
    exit 0
fi

models=("nomic-embed-text-v2" "ministral" "gpt-oss-safeguard")

for model in "${models[@]}"; do
    if ollama list | grep -q "$model"; then
        echo "Model '$model' already exists. Skipping."
    else
        echo "Pulling model: $model..."
        ollama pull "$model"
    fi
done

echo ""
echo "========================================"
echo " Environment Ready!"
echo "========================================"
echo "To start querying, run: python -m tools.rag.cli query \"your question\""
