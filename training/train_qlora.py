# training/train_qlora.py
import os, json
from datasets import load_dataset
from trl import SFTTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig

BASE_MODEL = os.getenv("BASE_MODEL", "Qwen/Qwen2.5-3B-Instruct")  # or meta-llama/Llama-3.2-3B-Instruct
TRAIN_PATH = os.getenv("TRAIN_PATH", "training/data/train.jsonl")
EVAL_PATH  = os.getenv("EVAL_PATH",  "training/data/eval.jsonl")
OUT_DIR    = os.getenv("OUT_DIR", "training/out-qlora")

print(f"Base model: {BASE_MODEL}")

ds = load_dataset("json", data_files={"train": TRAIN_PATH, "eval": EVAL_PATH})

def fmt(x):
    if x.get("input"):
        return f"### Instruction:\n{x['instruction']}\n\n### Input:\n{x['input']}\n\n### Response:\n{x['output']}"
    return f"### Instruction:\n{x['instruction']}\n\n### Response:\n{x['output']}"

ds = ds.map(lambda x: {"text": fmt(x)}, remove_columns=ds["train"].column_names)

tok = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=True)
tok.pad_token = tok.eos_token

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype="bfloat16",
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)
model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, quantization_config=bnb, device_map="auto")

peft = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj","v_proj","k_proj","o_proj"]
)

args = TrainingArguments(
    output_dir=OUT_DIR,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=8,
    num_train_epochs=1,
    learning_rate=2e-4,
    bf16=True,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=50,
    save_steps=100,
    save_total_limit=2,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine"
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tok,
    train_dataset=ds["train"],
    eval_dataset=ds.get("eval"),
    peft_config=peft,
    dataset_text_field="text",
    max_seq_length=1024,
    packing=True,
    args=args,
)

trainer.train()
trainer.model.save_pretrained(os.path.join(OUT_DIR, "adapter"))
tok.save_pretrained(os.path.join(OUT_DIR, "adapter"))
print("Saved PEFT adapter to", os.path.join(OUT_DIR, "adapter"))
