# Trying to connect to MySQL Database
import db_connection
import interface
import os

# Import libraries
import pandas as pd

parent_dir = os.path.dirname(os.getcwd())
product_dir = parent_dir + '\\Data\\processed_products.csv'
review_dir = parent_dir + '\\Data\\processed_reviews.csv'

# Main
if __name__ == "__main__":   
    # Read csv data
    df_product = pd.read_csv(product_dir)
    df_review = pd.read_csv(review_dir)
    
    # Rename df columns
    df_product.columns = [col.lower().replace(" ", "_") for col in df_product.columns]
    df_review.columns = [col.lower().replace(" ", "_") for col in df_review.columns]

    # Write Data to SQL
    db_connection.write_to_sql(df=df_product, name='products')
    db_connection.write_to_sql(df=df_review, name='reviews')
    
    # # # EInitialize DataFrame variables for querying
    df_list = [df_product, df_review]
    df_names = ['products', 'reviews']

    interface.create_interface(placeholder='Message Hasaski Chatbot...', df_list=df_list, df_names=df_names)
    