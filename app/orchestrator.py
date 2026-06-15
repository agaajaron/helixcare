import time
import json
from app.rag.index_builder import build_policy_index
from app.agents.prior_auth_agent import build_prior_auth_agent
from app.agents.summarizer_agent import build_summarizer_agent
from app.agents.eligibility_agent import build_eligibility_agent
from app.agents.provider_agent import build_provider_agent
from app.tools.codes_tools import ICD10_TOOL, CPT_TOOL
from app.tools.fhir_tools import COVERAGE_TOOL
from app.tools.provider_dir_tools import PROVIDER_TOOL
from app.llm import get_llm
from app.metrics import REQUESTS, ERRORS, CITATIONS, MISSING_CITATIONS, LATENCY, ensure_metrics_server

def run_mri_pa_flow(member_id: str, modality="MRI", symptom="low back pain", near_zip="80301"):
    ensure_metrics_server()
    REQUESTS.labels(flow="prior_auth").inc()
    _llm = get_llm()
    t0 = time.time()

    # 1) context
    coverage = COVERAGE_TOOL.fn(member_id)
    plan = coverage.get("plan_id", "PPO-Blue-2025")

    # 2) policy index and agents
    pindex = build_policy_index()
    pa_agent = build_prior_auth_agent(pindex, [ICD10_TOOL, CPT_TOOL], llm=_llm)
    elig_agent = build_eligibility_agent([COVERAGE_TOOL], llm=_llm)
    prov_agent = build_provider_agent([PROVIDER_TOOL], llm=_llm)
    sum_agent = build_summarizer_agent(llm=_llm)

    # 3) agent calls (LLM-backed; JSON-focused prompts)
    pa_json = pa_agent.chat(f"Is PA required for {modality} under plan {plan} for symptom '{symptom}'? Return JSON only.")
    elig_json = elig_agent.chat(f"Member {member_id} coverage details. Return JSON only.")
    providers_json = prov_agent.chat(f"Find in-network for {modality} under {plan} near {near_zip}. Return JSON only.")

    # 4) summarization (Why Card + member-facing text)
    summary = sum_agent.chat(
      f"Member {member_id}, plan {plan}.\nPA: ```{pa_json}```\nEligibility: ```{elig_json}```\nProviders: ```{providers_json}```\n"
      "Produce a concise summary with a Why Card JSON at the end."
    )

    # Metrics: latency & simple citation detection
    LATENCY.labels(flow="prior_auth").observe(time.time()-t0)
    if 'planRules#4.2' in str(summary):
        CITATIONS.inc()
    else:
        MISSING_CITATIONS.inc()

    return summary

if __name__ == "__main__":
    print(run_mri_pa_flow("M123"))
