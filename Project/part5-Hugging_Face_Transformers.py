from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "openchat/openchat-3.5-1210"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # 👈 Enable half-precision
    device_map="auto"
)