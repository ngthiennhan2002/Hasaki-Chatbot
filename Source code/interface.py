import streamlit as st
import pandas as pd
import db_connection
import text2sql

def create_interface(placeholder, df_list, df_names):
    # Streamlit Title
    st.title("Hasaki Chatbot")
        
    user_query = st.text_area(label="Enter your message", 
                                placeholder=placeholder)

    # Execution button
    if st.button(label="Send"):
        try:
            if user_query == "":
                st.text("Please enter your question.")
                
            else:   
                # Run Text to SQL
                sql_query = text2sql.gemini_text2sql_execution(user_query=user_query, df_list=df_list, df_names=df_names)
                df_result = db_connection.read_sql(sql_query=sql_query)
                st.text(sql_query)
                
                # Display response
                st.header("Response")
                st.text(f"This is the answer for the question \"{user_query}\"")
                for index, row in df_result.iterrows():
                    with st.container():
                        # Tạo các box cho mỗi sản phẩm
                        st.subheader(f"Product {index + 1}: {row['vn_name']}")  # Tiêu đề sản phẩm
                        st.image(f"{row['image']}", caption=row['vn_name'], width=150)  # Hiển thị hình ảnh (thay 'images/{row['image']}.jpg' bằng đường dẫn thực tế của bạn)

                        # Hiển thị các thông tin khác của sản phẩm
                        st.write(f"**Brand**: {row['brand']}")
                        st.write(f"**Category**: {row['category']}")
                        st.write(f"**Actual Price**: {row['actual_price']} VND")
                        st.write(f"**Discount Price**: {row['discount_price']} VND")
                        st.write(f"**Discount Rate**: {row['discount_rate']}%")
                        st.write(f"**Stars**: {row['star']} / 5")
                        st.write(f"**Rating**: {row['rating']} reviews")
                        st.write(f"**Sold**: {row['sold']} units")
                        st.write(f"[More Info]({row['link']})")  # Thêm link dẫn tới sản phẩm
                        st.markdown("---")  # Thêm một dòng phân cách giữa các sản phẩm
        except Exception as e:
            st.error(f"Error: {e}")