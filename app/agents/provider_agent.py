from llama_index.core.agent import ReActAgent

def build_provider_agent(tools, llm=None):
    sys_prompt = (
        "Find in-network providers for the requested modality and plan. "
        "Return JSON with fields: {providers:[{name, zip}]}."
    )
    return ReActAgent.from_tools(tools=tools, llm=llm, system_prompt=sys_prompt)
