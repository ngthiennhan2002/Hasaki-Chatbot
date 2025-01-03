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
    
    return response
