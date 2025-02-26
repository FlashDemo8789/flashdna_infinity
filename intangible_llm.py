import torch, re
from auto_gptq import AutoGPTQForCausalLM
from transformers import AutoTokenizer

MODEL_PATH = "./Llama-2-7B-Chat-GPTQ"

_tokenizer = None
_model = None

def load_llama():
    global _tokenizer, _model
    if _model is None:
        print("Loading Llama 2 GPTQ model ...")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        _model = AutoGPTQForCausalLM.from_quantized(
            MODEL_PATH,
            device_map="auto",
            torch_dtype=torch.float16
        )
    return _tokenizer, _model

def compute_intangible_llm(doc: dict)-> float:
    text= doc.get("pitch_deck_text","").strip()
    tokenizer, model= load_llama()

    # Make sure the triple-quoted string is closed properly:
    prompt = f"""You are a venture analysis AI.
Rate the intangible factors (passion, clarity, excitement) from 0..100 for this pitch deck:
{text}
Only return a numeric score, no explanation."""

    inputs= tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        out= model.generate(**inputs, max_new_tokens=50)
    resp= tokenizer.decode(out[0], skip_special_tokens=True)

    # Parse numeric from LLM output
    matches = re.findall(r"\b(\d{1,3})\b", resp)
    val = 50.0
    if matches:
        score = float(matches[-1])
        if 0 <= score <= 100:
            val = score
    return val