"""
LLM Models module for DigiTwin Analytics
Contains AI model interactions and response generation logic
"""

import os
import time
import openai
from cerebras.cloud.sdk import Cerebras
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils import log_execution
from config import MODEL_CONFIGS, PROMPTS

# --- LLM RESPONSE LOGIC ---
@log_execution
def generate_response(prompt, model_alias, prompt_type, df=None, vectorstore=None):
    """Generate response using the selected AI model"""
    messages = [{"role": "system", "content": PROMPTS[prompt_type]}]
    
    # Add context from PDF reports if available
    if vectorstore:
        docs = vectorstore.similarity_search(prompt, k=5)
        context = "\n\n".join([doc.page_content for doc in docs])
        messages.append({"role": "system", "content": f"Context from PDF reports:\n{context}"})
    
    # Add Excel data summary if available
    if df is not None:
        summary = df.describe().to_string()
        messages.append({"role": "system", "content": f"Excel data summary:\n{summary}"})
    
    messages.append({"role": "user", "content": prompt})
    full_response = ""

    try:
        config = MODEL_CONFIGS[model_alias]
        
        if config["provider"] == "openai":
            return _handle_openai_response(config, messages)
        elif config["provider"] == "cerebras":
            return _handle_cerebras_response(config, messages)
        elif config["provider"] == "huggingface":
            return _handle_huggingface_response(config, messages, prompt_type, prompt)
        else:
            yield f"<span style='color:red'>⚠️ Error: Unknown provider {config['provider']}</span>"
            
    except Exception as e:
        yield f"<span style='color:red'>⚠️ Error: {str(e)}</span>"

def _handle_openai_response(config, messages):
    """Handle OpenAI-based model responses"""
    client = openai.OpenAI(
        api_key=os.getenv(config["api_key_env"]), 
        base_url=config["base_url"]
    )
    response = client.chat.completions.create(
        model=config["model"], 
        messages=messages, 
        stream=config["stream"]
    )
    
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            delta = chunk.choices[0].delta.content
            yield f"<span style='font-family:Tw Cen MT'>{delta}</span>"

def _handle_cerebras_response(config, messages):
    """Handle Cerebras model responses"""
    client = Cerebras(api_key=os.getenv(config["api_key_env"]))
    response = client.chat.completions.create(
        model=config["model"], 
        messages=messages
    )
    content = response.choices[0].message.content if hasattr(response.choices[0], "message") else str(response.choices[0])
    
    for word in content.split():
        yield f"<span style='font-family:Tw Cen MT'>{word} </span>"
        time.sleep(0.01)

def _handle_huggingface_response(config, messages, prompt_type, prompt):
    """Handle HuggingFace model responses"""
    model_id = config["model_id"]
    tokenizer = AutoTokenizer.from_pretrained(
        model_id, 
        trust_remote_code=True, 
        token=os.getenv(config["api_key_env"])
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        trust_remote_code=True, 
        device_map="auto", 
        token=os.getenv(config["api_key_env"])
    )
    
    if "XAI Inspector" in config["model_id"]:
        input_ids = tokenizer.apply_chat_template(messages, return_tensors="pt").to(model.device)
        output = model.generate(input_ids, max_new_tokens=512, do_sample=True, top_p=0.9)
    else:  # Valonys Llama
        input_ids = tokenizer(PROMPTS[prompt_type] + "\n\n" + prompt, return_tensors="pt").to(model.device)
        output = model.generate(**input_ids, max_new_tokens=512)
    
    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    yield f"<span style='font-family:Tw Cen MT'>{decoded}</span>" 