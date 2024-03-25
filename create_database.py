import mysql.connector
from mysql.connector import errorcode
from config import mysql_user, mysql_password, mysql_hostname, mysql_database_name, mysql_table_name


# Connect to MySQL server
try:
    cnx = mysql.connector.connect(host=mysql_hostname, user=mysql_user, password=mysql_password)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("User name or password incorrect")
    else:
        print(err)
    # Close connection (ensure it's closed even in case of errors)
    cnx.close()
    print('Connection closed')

# Instantiate cursor object
cursor = cnx.cursor()

# Create database (mysql_database_name) if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(mysql_database_name))

# Use given database
cursor.execute("USE {}".format(mysql_database_name))


# Create table with sensor data columns (use existing connection)
create_table_sql = f"""CREATE TABLE IF NOT EXISTS {mysql_table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Temperature FLOAT,
    Humidity FLOAT,
    Light FLOAT,
    CO2 FLOAT,
    HumidityRatio FLOAT,
    Occupancy INT
)"""

cursor.execute(create_table_sql)

print(f"Table '{mysql_table_name}' created successfully in database '{mysql_database_name}'.")



