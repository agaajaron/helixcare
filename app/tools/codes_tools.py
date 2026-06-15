from llama_index.core.tools import FunctionTool
import pandas as pd

_icd = pd.read_csv("data/codes/icd10.csv")
_cpt = pd.read_csv("data/codes/cpt.csv")

def lookup_icd10(term: str):
    hits = _icd[_icd["desc"].str.contains(term, case=False, na=False)]
    return hits.head(5).to_dict(orient="records")

def lookup_cpt(term: str):
    hits = _cpt[_cpt["desc"].str.contains(term, case=False, na=False)]
    return hits.head(5).to_dict(orient="records")

ICD10_TOOL = FunctionTool.from_defaults(fn=lookup_icd10, name="lookup_icd10", description="Search ICD-10 by text")
CPT_TOOL   = FunctionTool.from_defaults(fn=lookup_cpt,   name="lookup_cpt",   description="Search CPT/HCPCS by text")
