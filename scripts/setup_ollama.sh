#!/usr/bin/env bash
set -euo pipefail

if ! command -v ollama &>/dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

echo "Pulling models..."
ollama pull qwen2.5:7b

echo "Ollama setup complete!"
echo "Start server with: ollama serve"
