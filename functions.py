import cx_Oracle
import pandas as pd
import oracledb

# These two lines of code are needed for the Oracle client to work on my Windows machine. If you are on windows,
    # replace the path with the path to your Oracle Instant Client (the path you added as an environment variable).
    # Otherwise, comment it out and disregard.
path_of_oracle_instant_client = r"D:\Program Files\Oracle\instantclient_21_9"
cx_Oracle.init_oracle_client(lib_dir=path_of_oracle_instant_client)

def query_db(sql_query):

    #doc way
    # cs='''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.us-ashburn-1.oraclecloud.com))(connect_data=(service_name=gcce3a0711f9852_ofvc0afuiao4hmzy_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''

    # conn=oracledb.connect(
    #  user="williamsobczak",
    #  password="WorldLivesOn123",
    #  dsn=cs)
    





    # # #old way
    # user = 'williamsobczak'
    # password = 'WorldLivesOn123'
    # connection_string = '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.us-ashburn-1.oraclecloud.com))(connect_data=(service_name=gcce3a0711f9852_ofvc0afuiao4hmzy_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'

    # # #Connect to Oracle Database
    # conn = cx_Oracle.connect(user = user, password = password, dsn = connection_string)






    #chat way

    # replace with your credentials and connection information
    # dsn = cx_Oracle.makedsn("adb.us-ashburn-1.oraclecloud.com", "1522", service_name="gcce3a0711f9852_ofvc0afuiao4hmzy_high.adb.oraclecloud.com")
    # username = "williamsobczak"
    # password = "WorldLivesOn123"

    # establish the connection
    #conn = cx_Oracle.connect(user=username, password=password, dsn=dsn)







    #try again

    # dsn = cx_Oracle.makedsn("adb.us-ashburn-1.oraclecloud.com", "1521", service_name="gcce3a0711f9852_ofvc0afuiao4hmzy_high.adb.oraclecloud.com")
    # conn = cx_Oracle.connect("williamsobczak", "WorldLivesOn123", dsn=dsn)








    #try again
    # Replace the placeholders with your actual values
    # username = "williamsobczak"
    # password = "WorldLivesOn123"
    # dsn = oracledb.makedsn(
    #     "adb.us-ashburn-1.oraclecloud.com",
    #     1521,
    #     service_name="gcce3a0711f9852_ofvc0afuiao4hmzy_high.adb.oraclecloud.com",
    # )

    # Connect to the database
    # conn = oracledb.connect(user=username, password=password, dsn=dsn)








    #try again

    # conStr = 'williamsobczak/WorldLivesOn123@adb.us-ashburn-1.oraclecloud.com:1522/gcce3a0711f9852_ofvc0afuiao4hmzy_high.adb.oraclecloud.com'
    # conn = cx_Oracle.connect(conStr)






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