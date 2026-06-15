from llama_index.core.tools import FunctionTool
import json, glob

def get_coverage(member_id: str):
    for p in glob.glob("data/fhir/coverage_*.json"):
        cov = json.load(open(p))
        if cov.get("member_id") == member_id:
            return cov
    return {"error": "not_found"}

COVERAGE_TOOL = FunctionTool.from_defaults(
    fn=get_coverage, name="get_member_coverage",
    description="Fetch member coverage by member_id (synthetic)"
)
