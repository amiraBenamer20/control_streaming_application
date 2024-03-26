import findspark
findspark.init('/home/amira/Téléchargements/spark-3.5.1-bin-hadoop3')  


from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types
#from kafka import KafkaConsumer
from config import mysql_database_name, mysql_table_name, mysql_hostname, mysql_port
from config import  mysql_user, mysql_password, kafka_config
from process_data import process_sensor_data
from predict import training_prediction, use_existing_model

mysql_driver = 'com.mysql.jdbc.Driver'
mysql_jdbc_url = 'jdbc:mysql://' + mysql_hostname + ':' + mysql_port + '/' + mysql_database_name




# Spark session configuration
spark = SparkSession.builder \
  .master("local")\
  .appName("Data_Streaming") \
  .config("spark.jars", "jars/spark-sql-kafka-0-10_2.12-3.5.0.jar,"\
          "jars/spark-sql_2.12-3.5.1.jar,"\
        "jars/kafka-clients-3.5.0.jar,"\
        "jars/spark-streaming-kafka-0-10-assembly_2.12-3.5.0.jar,"\
        "jars/mysql-connector-java-5.1.48.jar," \
        "jars/commons-pool2-2.12.0.jar,")\
  .config("spark.driver.extraClassPath", "jars/spark-sql-kafka-0-10_2.12-3.5.0.jar,"\
        "jars/kafka-clients-3.5.0.jar,"\
        "jars/spark-streaming-kafka-0-10-assembly_2.12-3.5.0.jar,"\
        "jars/mysql-connector-java-5.1.48.jar," \
        "jars/commons-pool2-2.12.0.jar,")\
    .getOrCreate()

# Set log level
spark.sparkContext.setLogLevel("ERROR")

def write_stream_to_mysql(dataFrame, id):
    """Writes each batch of streaming dataFrame to MySQL/MariaDB
    
    """

    print("------------------------herrrrrrrrrrrrre-------------")
    dataFrame = training_prediction(dataFrame)

    print("heeeeeeeeeeeeeeeeelllllllllllo")
    db_properties = {"user": mysql_user,
        "password": mysql_password,
        "driver": mysql_driver}

    if dataFrame.rdd.isEmpty():
        print("?????????????????????????????????????????????????")
    else:
        dataFrame \
          .write \
          .jdbc(url=mysql_jdbc_url,
            table=mysql_table_name,
            mode='append',
            properties=db_properties)
        print("yaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaay")





# Kafka consumer configuration
# consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
#                          group_id='sensor-data-consumer',
#                          auto_offset_reset='earliest')
# consumer.subscribe(kafka_config['topics'][0])  


# Create a streaming DataFrame from kafka
"""
root
 |-- key: binary (nullable = true)
 |-- value: binary (nullable = true)
 |-- topic: string (nullable = true)
 |-- partition: integer (nullable = true)
 |-- offset: long (nullable = true)
 |-- timestamp: timestamp (nullable = true)
 |-- timestampType: integer (nullable = true)
"""

schema = types.StructType([
    types.StructField('data', types.StringType()),
    types.StructField('Timestamp', types.StringType())
])


schema_2 = types.StructType([
      types.StructField("Temperature", types.FloatType(), True),
      types.StructField("Humidity", types.FloatType(), True),
      types.StructField("Light", types.FloatType(), True),
      types.StructField("CO2", types.FloatType(), True),
      types.StructField("HumidityRatio", types.FloatType(), True),
      #types.StructField("Occupancy", types.IntegerType(), True),
  ])

stream = spark.readStream.format("kafka") \
  .option("kafka.bootstrap.servers", ", ".join(kafka_config['servers']))\
  .option("subscribe", kafka_config['topics'][1]) \
  .option("startingOffsets", "earliest") \
  .option("failOnDataLoss", "false") \
  .load()\
 .selectExpr("CAST(value AS STRING)") \
  .select(F.from_json(F.col("value"), schema_2).alias("data")) \
  .select("data.*")

  #.select("timestamp", "data.timestamp") \
  #withColumn("Timestamp", F.to_timestamp(F.col("Timestamp"), "yyyy-MM-dd HH:mm:ss")) \
  #.drop("Timestamp")

stream.printSchema()
print(type(stream))


# Process the streaming DataFrame
processed_stream = process_sensor_data(stream)

# Start the streaming query
"""query = processed_stream \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()"""



# Start streaming query
query = processed_stream\
  .option("checkpointLocation", "/tmp/spark-checkpoint8") \
  .outputMode('append') \
  .foreachBatch(use_existing_model) \
  .start()


# Wait for termination signal
query.awaitTermination()


"""
# Assuming you have a SparkSession initialized (spark) and a Spark DataFrame (spark_df) for room sensor data

# Example usage (apply models)
for model_name in [
    ["Logistic Regression", "LR"],
    ["DecisionTree", "DT"],
    ["Random Forest", "RF"],
    ["K-Nearest Neighbors", "KNN"],
    ["Naive Bayes", "NB"],
    ["Support Vector Machine", "SVM"],
    ["Gradient Boosting", "GB"],
    ["Multi-Layer Perceptron", "MLP"],
]:
"""





