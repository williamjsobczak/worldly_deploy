import cx_Oracle
import pandas as pd
import oracledb

# These two lines of code are needed for the Oracle client to work on my Windows machine. If you are on windows,
    # replace the path with the path to your Oracle Instant Client (the path you added as an environment variable).
    # Otherwise, comment it out and disregard.
path_of_oracle_instant_client = r"D:\Program Files\Oracle\instantclient_21_9"
cx_Oracle.init_oracle_client(lib_dir=path_of_oracle_instant_client)

def query_db(sql_query):

    #with wallet

    conn=oracledb.connect(
     user="williamsobczak",
     password="WorldLivesOn123",
     dsn="ofvc0afuiao4hmzy_low",
     config_dir="Wallet_OFVC0AFUIAO4HMZY-3",
     wallet_location="Wallet_OFVC0AFUIAO4HMZY-3",
     wallet_password="WorldLivesOn123")


    #the rest of it
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()

    df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
    cursor.close()
    conn.close()

    return df

def reformat_data_label(label):
    words = label.split('_')
    formatted_words = [word.lower().capitalize() for word in words]
    return ' '.join(formatted_words)

def format_attribute_name_for_sql(attribute_name):
    return attribute_name.replace(' ', '_').upper()