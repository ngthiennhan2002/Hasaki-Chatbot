import requests
from dotenv import load_dotenv
import os
import torch
from transformers import pipeline

load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
dialect = os.getenv("API_DIALECT")

# Function to convert text to SQL
def execution(user_query, df_list, df_names):
    # Check if the lengths of the df_list and df_names are equal:
    if len(df_list) != len(df_names):
        return "Error with df_list and df_names (may have different lengths)."
    
    # Create database tables
    tables = []
    for i in range(len(df_list)):
        tables.append(
            {
                "name": df_names[i],
                "columns": df_list[i].columns.tolist()
            },
        )
        
    # Run execution
    user_query += str(tables)
    user_query += "Chỉ trả về kết quả mã SQL, không trả về bất cứ thông tin nào khác."
    messages = [
        {"role": "user", "content": user_query},
    ]
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_name = "Qwen/Qwen2.5-Coder-32B-Instruct"

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    messages = [
        {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
        {"role": "user", "content": user_query}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return response
