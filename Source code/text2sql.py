import requests
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
dialect = os.getenv("API_DIALECT")


# Function to convert text to SQL
def gemini_text2sql_execution(user_query, df_list, df_names):
    # Function to get SQL result in the response
    def response_processing(response):
        sql_code = response._result.candidates[0].content.parts[0].text.strip()
        if sql_code.startswith("```sql"):
            sql_code = sql_code[6:]  # Bỏ phần "```sql\n"
        if sql_code.endswith("```"):
            sql_code = sql_code[:-3]  # Bỏ phần "```"
        return sql_code
    
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
        
    # User query
    user_query += str(tables)
    
    category_query = user_query + ". Tìm category được nêu trong câu trên và chỉ nêu ra category."
    
    # Text-to-SQL execution
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    category = model.generate_content(category_query)
    category = str(response_processing(response=category)).lower()
    print(category)
    
    user_query += f"Chỉ trả về kết quả mã SQL, không trả về bất cứ thông tin nào khác.\
        Ghi liền một chuỗi không xuống dòng nhưng vẫn giữ SPACE.\
        Trường hợp nếu chỉ hỏi Sản phẩm nào thì trả về tất cả thông tin SELECT *.\
        Nhận biết loại sản phẩm '{category}' trong câu input -> thêm vào câu sau: WHERE category REGEXP '\\bmặt nạ\\b' OR WHERE vn_name REGEXP '\\bmặt nạ\\b' OR WHERE en_name REGEXP '\\bmặt nạ\\b'\
        với bước nhận biết đầu tiên là quan trọng nhất"
    response = model.generate_content(user_query)
    
    # Processing response to get text
    result = response_processing(response=response)
    return result
