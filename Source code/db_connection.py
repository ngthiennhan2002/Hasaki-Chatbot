from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pandas as pd

# Create connection
def get_connection():
    load_dotenv()
    password = os.getenv("DB_PASSWORD")
    user = os.getenv("DB_USER")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    
    # Create an engine to save DataFrame to SQL
    db_connection_str = f'mysql+pymysql://{user}:{password}@{host}/{database}'
    engine = create_engine(db_connection_str)
    return engine


# Write a DataFrame to MySQL
def write_to_sql(df, name):
    try:
        # Create a SQL engine
        engine = get_connection()
        
        # Save to SQL, if any data exists then replace the old data
        df.to_sql(name=name, con=engine, if_exists="replace", index=False)
        print(f"Saved '{name}' table successfully.")
    except:
        print("Error while saving a Dataframe to MySQL")
        
        
# Read MySQL data, then save results in a DataFrame
def read_sql(sql_query):
    try:
        # Create a SQL engine
        engine = get_connection()
        
        # Save to SQL, if any data exists then replace the old data
        df_result = pd.read_sql(sql_query, con=engine)
        return df_result
    except Exception as e:
        print(f"Error: {e}")
        return None