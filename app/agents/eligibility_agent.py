from llama_index.core.agent import ReActAgent

def build_eligibility_agent(tools, llm=None):
    sys_prompt = (
        "Check coverage status, deductible, and OOP using tools only. "
        "Return JSON with fields: {active: bool, deductible_remaining: number, oop_remaining: number}."
    )
    return ReActAgent.from_tools(tools=tools, llm=llm, system_prompt=sys_prompt)
