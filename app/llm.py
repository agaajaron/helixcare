
import os
from typing import Optional

def get_llm():
    """Return a LlamaIndex LLM instance.
    If LLAMA_CPP_MODEL_PATH is set, use llama-cpp; otherwise fallback to OpenAI (requires OPENAI_API_KEY).
    """
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
