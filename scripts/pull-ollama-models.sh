#!/bin/bash
# Script to pull Ollama models after container starts

echo "🤖 Pulling Ollama models..."

# Wait for Ollama service to be ready
echo "⏳ Waiting for Ollama service to start..."
sleep 10

# Pull gemma3:4b (default model)
echo "📥 Pulling gemma3:4b (recommended for production)..."
ollama pull gemma3:4b

# Pull qwen3:4b as alternative
echo "📥 Pulling qwen3:4b (alternative model)..."
ollama pull qwen3:4b

echo "✅ Model download complete!"
echo ""
echo "Available models:"
ollama list

echo ""
echo "🎵 Models ready for MusicMood!"
echo "   - gemma3:4b (default, 3.3GB)"
echo "   - qwen3:4b (alternative, 2.5GB)"
echo "   - phi3:3.8b (Microsoft, instruction-tuned)"
