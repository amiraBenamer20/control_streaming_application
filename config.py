


# Specify Kafka brokers addresses and topics
kafka_config = {'servers':['localhost:9092','localhost:9093','localhost:9094'], 'topics': ['room_sensor_data_streams','incoming_streams']}#others may be added..



# Database (MySQL/MariaDB) properties
mysql_user = 'root'
mysql_password = 'password'

mysql_hostname = '127.0.0.1'
mysql_port = '3306'

mysql_database_name = 'sensor_data_new'
mysql_table_name = 'sensor_data_joined'