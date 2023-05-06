import cx_Oracle
import pandas as pd

# These two lines of code are needed for the Oracle client to work on my Windows machine. If you are on windows,
    # replace the path with the path to your Oracle Instant Client (the path you added as an environment variable).
    # Otherwise, comment it out and disregard.
path_of_oracle_instant_client = r"D:\Program Files\Oracle\instantclient_21_9"
cx_Oracle.init_oracle_client(lib_dir=path_of_oracle_instant_client)

def query_db(sql_query):

    # Connect to Oracle Database
    conn = cx_Oracle.connect(user='williamsobczak', password='REBY7TpizLTdOp5dZHa9qJS0',
                            dsn=cx_Oracle.makedsn('oracle.cise.ufl.edu', '1521',
                                                sid='orcl'))
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