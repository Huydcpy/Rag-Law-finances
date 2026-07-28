from llama_index.llms.ollama import Ollama

from src.configs.settings import LLM_MODEL_NAME, OLLAMA_BASE_URL

llm = Ollama(
    model=LLM_MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
)