# import libraries
from os import getcwd
import sqlite3
import pandas as pd

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn

# make connection to sqlite db
conn = create_connection('build/data/db.sqlite3')

# if connection has been succesfully established start extraction and transformation steps
if conn is not None:

    print("Making connection to database")

    # with active connection read database into pandas DataFrame using SQL statement
    df = pd.read_sql('SELECT * FROM rest_api_netlify', con=conn)
    
    # remove duplicates
    df = df[~df.duplicated()]

    # drop rows with missing data
    df = df.dropna()

    # Adding bmi as new feature [bmi = mass / length^2]
    df['bmi'] = round(df['mass'] / (df['length']/100)**2,1)
    # reorder columns to put lifespan at the end
    df_cleaned = df.reindex(columns=['genetic', 'length', 'mass', 'bmi', 'exercise', 'smoking', 'alcohol', 'sugar', 'lifespan'])

    # Calculating Interquartile Range [1.5] to remove mathematical outliers
    Q1 = df_cleaned.quantile(0.25)
    Q3 = df_cleaned.quantile(0.75)
    IQR = Q3 - Q1
    df_iqr_cleaned = df_cleaned[~((df_cleaned < (Q1 - 1.5 * IQR)) |(df_cleaned > (Q3 + 1.5 * IQR))).any(axis=1)]

    # save dataframes to sqlite3 table
    df_cleaned.to_sql('data_cleaned', con=conn, index=False)
    df_iqr_cleaned.to_sql('data_iqr_cleaned', con=conn, index=False)

    # save to csv file
    df_cleaned.to_csv('build/data/data_cleaned.csv', index=False)
    df_iqr_cleaned.to_csv('build/data/data_cleaned.csv', index=False)

    conn.close()
    
# if connections cannot be established, print message to user
else:
    print("Error! Cannot create the database connection.")

