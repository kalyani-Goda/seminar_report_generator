import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_WRITER_MODEL = os.getenv("OLLAMA_WRITER_MODEL","qwen3:8b")
OLLAMA_CRITIC_MODEL = os.getenv("OLLAMA_CRITIC_MODEL","deepseek-r1")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL","nomic-embed-text")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY","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")