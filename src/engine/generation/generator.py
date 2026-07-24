from llama_index.llms.ollama import Ollama

llm = Ollama(
    model="qwen2.5:7b",
    base_url="http://localhost:11434",
)