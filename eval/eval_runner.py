import json, re
from jsonschema import validate
from app.orchestrator import run_mri_pa_flow

WHY_SCHEMA = {
  "type": "object",
  "properties": {
    "decision": {"type": "string"},
    "sources": {"type": "array"},
    "criteria": {"type": "array"}
  },
  "required": ["decision", "sources"]
}

def extract_json(text: str):
    import re, json
    m = re.findall(r"\{[\s\S]*\}$", text.strip())
    if not m: return None
    try: return json.loads(m[-1])
    except Exception: return None

def run_eval():
    rows = [json.loads(l) for l in open("eval/test_sets/pa_queries.jsonl") if l.strip()]
    valid = 0
    for ex in rows:
        out = run_mri_pa_flow(ex["member_id"], ex["modality"], ex["symptom"], ex["zip"])
        why = extract_json(out)
        if why:
            try:
                validate(why, WHY_SCHEMA); valid += 1
            except Exception as e:
                print("Schema error:", e)
    print("Why Card valid:", f"{valid}/{len(rows)}")

if __name__ == "__main__":
    run_eval()
