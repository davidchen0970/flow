import mysql.connector
from mysql.connector import errorcode


config = {

    'host': '********.mysql.database.azure.com',
    'user': '********',
    'password': '********',
    'database': 'first',
    'client_flags': [mysql.connector.ClientFlag.SSL],
    'ssl_ca': 'DigiCertGlobalRootCA.crt.pem'
}

# Construct connection string

try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = conn.cursor()

    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS inventory;")
    print("Finished dropping table (if existed).")

    # Create table
    cursor.execute(
        "CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
    print("Finished creating table.")

    # Insert some data into table
    cursor.execute(
        "INSERT INTO test_crawler (id ,room,ip,flow,date) VALUES (%s, %s, %s, %s, %s);", ('1','6401A','10.10.66.30','123,456,789','2022012012'))
    print("Inserted", cursor.rowcount, "row(s) of data.")

    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")
