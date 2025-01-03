# Trying to connect to MySQL Database
import db_connection
import text2sql

# Import libraries
import pandas as pd
        
# Main
if __name__ == "__main__":   
    # Read csv data
    df_product = pd.read_csv("Data/processed_products.csv")
    df_review = pd.read_csv("Data/processed_reviews.csv")

    # Write Data to SQL
    db_connection.write_to_sql(df=df_product, name='products')
    db_connection.write_to_sql(df=df_review, name='reviews')
    
    # EInitialize DataFrame variables for querying
    df_list = [df_product, df_review]
    df_names = ['products', 'reviews']
    
    # Execute to get SQL query from an user_query
    user_query = "Hãy tìm cho tôi top 10 sản phẩm có lượt bán cao nhất"
    sql_query = text2sql.execution(user_query=user_query, df_list=df_list, df_names=df_names)
    print(sql_query)
    
    # Show output
    # df_result = db_connection.read_sql(sql_query=sql_query)
    # print(df_result)