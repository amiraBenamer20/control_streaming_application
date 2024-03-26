import csv
from kafka import KafkaProducer
import json
from config import kafka_config
import time

# Kafka producer configuration
producer = KafkaProducer(bootstrap_servers='localhost:9092')


training = 0 #0 means use faker to generate data, 1 means publish training data since this is the first time to publish data

# Path to your CSV file
#This should be executed when the the application is launched for the first time where data will be the the training dataset in the prediction phase
data_file = 'Dataset/Occupancy.csv'

# Function to read CSV data and publish to Kafka
def publish_sensor_data():
  with open(data_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    #time.sleep(5)
    for row in reader:
      # Serialize data as JSON (modify as needed for your data)
      data = {'Temperature': float(row['Temperature']),
              'Humidity': float(row['Humidity']),
              'Light': float(row['Light']),
              'CO2': float(row['CO2']),
                'HumidityRatio': float(row['HumidityRatio']),
               #'Occupancy': int(row['Occupancy'])
                }
                
      
      #publish to "sensor_data topic: data"   
      # !!!we can divide this to different topics (temperature, humidity, light..)
      producer.send(kafka_config['topics'][1], json.dumps(data).encode('utf-8'))
      print(f"Published data: {data}")
      time.sleep(5)
      


if __name__ == '__main__':
  publish_sensor_data()