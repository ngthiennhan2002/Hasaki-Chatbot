import streamlit as st
import pandas as pd
import db_connection
import text2sql

questions = []
answers = []

def show_chat(questions, answers):
    product_box_style = """
    <style>
        .product-box {
            background-color: rgba(255,255,255);  /* Màu trắng */
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            color: black;  /* Màu chữ đen */
        }
        .product-box img {
            width: 100px;
            height: 100px;
            object-fit: cover;
            border-radius: 8px;
            margin-right: 15px;
        }
        .product-box .product-info {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .product-box h3, .product-box p {
            color: black;  /* Đảm bảo chữ màu đen */
        }
    </style>
    """
    # Display bubble chat
    num_questions = len(questions)
    
    for index in range(num_questions - 1, -1, -1):
        # Show question
        question = questions[index]
        st.markdown(f"""
        <div style="background-color: #004000; color: white; padding: 10px; border-radius: 10px; 
                    text-align: right; max-width: 75%; width: auto; height: auto;
                    margin-left: auto; margin-right: 0;
                    word-wrap: break-word; display: inline-block;">
            <strong>{question}</strong>
        </div>
        """, unsafe_allow_html=True)

        # Display answers
        st.markdown(product_box_style, unsafe_allow_html=True)
        answer = answers[index]
        st.markdown(answer, unsafe_allow_html=True)
    

def create_interface(placeholder, df_list, df_names):
    # Streamlit page
    st.set_page_config(page_title="Hasaki Chatbot", page_icon=":shopping_cart:", layout="wide")
    
    # Streamlit Title
    st.title("Hasaki Chatbot")
    
    # User input area
    user_query = st.text_area(label="Enter your message", placeholder=placeholder)

    # Execution button
    if st.button(label="Send"):
        if user_query == "":
            st.text("Please enter your question.")
        else:
            try:
                # Save the question to the session state
                questions.append(user_query)

                # Run Text to SQL (assume text2sql.gemini_text2sql_execution is valid)
                sql_query = text2sql.gemini_text2sql_execution(user_query=user_query, df_list=df_list, df_names=df_names)
                df_result = db_connection.read_sql(sql_query=sql_query)
                
                full_answer = ""

                # Get the answer and add to the session state
                for index, product in df_result.iterrows():
                    full_answer += f"""
                        <div class="product-box">
                            <div style="display: flex; align-items: center;">
                                <img src="{product['image']}" alt="Product Image" style="width:300px; height:300px">
                                <div class="product-info">
                                    <a href="{product['link']}" target="_blank"><h3>{product['vn_name']}</h3></a>
                                    <p><strong>EN Name:</strong> {product['en_name']}</p>
                                    <p><strong>Brand:</strong> {product['brand']}</p>
                                    <p><strong>Category:</strong> {product['category']}</p>
                                    <p><strong>Actual Price:</strong> {product['actual_price']} VNĐ</p>
                                    <p><strong>Discount Price:</strong> {product['discount_price']} VNĐ</p>
                                    <p><strong>Discount Rate:</strong> {product['discount_rate']}%</p>
                                    <p><strong>Star:</strong> {product['star']}</p>
                                    <p><strong>Rating:</strong> {product['rating']}</p>
                                    <p><strong>Sold:</strong> {product['sold']}</p>
                                </div>
                            </div>
                        </div>
                        """
                answers.append(full_answer)
                
                # Show the chat history
                show_chat(questions, answers)
    
            except Exception as e:
                st.error(f"Error: {e}")
