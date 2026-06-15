from llama_index.core.agent import ReActAgent

def build_summarizer_agent(llm=None):
    sys_prompt = (
      "Create a member-friendly summary and a Why Card JSON: "
      "{decision, sources:[{doc_id, span}], criteria:[{id, met, evidence}]}."
      "If evidence is insufficient, state that and list missing docs."
    )
    return ReActAgent.from_tools(tools=[], llm=llm, system_prompt=sys_prompt)
