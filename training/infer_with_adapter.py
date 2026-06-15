# training/infer_with_adapter.py
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

BASE_MODEL = os.getenv("BASE_MODEL", "Qwen/Qwen2.5-3B-Instruct")
ADAPTER = os.getenv("ADAPTER", "training/out-qlora/adapter")

bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype="bfloat16", bnb_4bit_quant_type="nf4")
tok = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=True)
base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, quantization_config=bnb, device_map="auto")
model = PeftModel.from_pretrained(base, ADAPTER)

def gen(instr, inp=""):
    if inp:
        prompt = f"### Instruction:\n{instr}\n\n### Input:\n{inp}\n\n### Response:\n"
    else:
        prompt = f"### Instruction:\n{instr}\n\n### Response:\n"
    out = model.generate(**tok(prompt, return_tensors="pt").to(model.device), max_new_tokens=256)
    print(tok.decode(out[0], skip_special_tokens=True))

if __name__ == "__main__":
    gen("Does MRI need PA?", "Plan PPO-Blue-2025, CPT 72148, PT 6 weeks.")
