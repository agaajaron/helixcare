
import os
from typing import Optional

def get_llm():
    """Return a LlamaIndex LLM instance.
    Picks a backend based on available env vars:
    - ANTHROPIC_API_KEY -> Claude (Anthropic)
    - LLAMA_CPP_MODEL_PATH -> local llama.cpp model
    - otherwise -> OpenAI (requires OPENAI_API_KEY)
    """
    if os.getenv("ANTHROPIC_API_KEY"):
        from llama_index.llms.anthropic import Anthropic
        return Anthropic(model="claude-sonnet-4-6")

    model_path = os.getenv("LLAMA_CPP_MODEL_PATH")
    if model_path and os.path.exists(model_path):
        from llama_index.llms.llama_cpp import LlamaCPP
        return LlamaCPP(
            model_path=model_path,
            temperature=0.2,
            max_new_tokens=512,
            context_window=4096,
        )
    from llama_index.llms.openai import OpenAI
    return OpenAI(model="gpt-4o-mini")
