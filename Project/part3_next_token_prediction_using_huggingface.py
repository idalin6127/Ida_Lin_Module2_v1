from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login

#login(token="Your_hf_token")  # optional if already logged in via CLI

# you have to visit https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1 to sign the agreement in order to use this model
model_name = "mistralai/Mistral-7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
#model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=True, device_map="auto")


# Run model with torch_dtype=torch.float16 for O1  ---run with GPU
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")