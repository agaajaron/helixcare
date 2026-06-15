from llama_index.core.agent import ReActAgent
from llama_index.core import VectorStoreIndex
from llama_index.core.tools import QueryEngineTool

def build_prior_auth_agent(policy_index: VectorStoreIndex, tools, llm=None):
    query_engine = policy_index.as_query_engine(similarity_top_k=6, llm=llm)
    policy_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name="search_plan_policies",
        description="Search plan rules and prior-authorization policy documents for relevant criteria and citations.",
    )
    sys_prompt = (
        "You determine if prior authorization (PA) is required based on plan rules.\n"
        "Only answer using retrieved evidence; quote rule text snippets.\n"
        "Return JSON with fields: {requires_pa: bool, criteria: [..], quotes: [..]}."
    )
    agent = ReActAgent.from_tools(
        tools=[*tools, policy_tool],
        llm=llm,
        system_prompt=sys_prompt,
    )
    return agent
