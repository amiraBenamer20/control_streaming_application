
<h1><strong>IoT-based Indoor Occupancy Detection</strong></h1>

<h2>Introduction</h2>

​ Person detection in an embedded IoT device without the use of a computer vision solution refers to the ability to detect the presence of a person in a given environment using sensors and signal processing techniques instead of relying on visual image analysis. ​ Typically, this type of person detection solution is achieved by leveraging various types of sensors, such as passive infrared (PIR) sensors, ultrasonic sensors, and radar sensors, which can detect physical changes in the environment caused by the presence of a person, such as body heat or movement. ​ Signal processing techniques are then applied to the sensor data to detect and differentiate the signal patterns associated with a person's presence from other environmental noise. Machine learning algorithms may also be used to improve the accuracy of the person detection system. ​ By using sensors and signal processing techniques, this type of person detection system can be implemented in an embedded IoT device with limited computing resources, making it suitable for a wide range of applications, such as home automation, security systems, and smart buildings. ​ ​
Reading Dataset

This dataset is used for binary classification and contains experimental data related to the likelihood of a room being occupied based on five environmental factors: temperature, humidity, light, and carbon dioxide (CO2) and humidity ratio levels.

The dataset consists of five features and a target variable. The features are temperature, humidity, light,humidity ratio and CO2 levels, while the target variable indicates the likelihood of room occupancy.

A target value of 1 indicates that the room is likely to be occupied, while a target value of 0 indicates that the room is not likely to be occupied.


https://www.kaggle.com/code/ashrafsharifi/iot-based-indoor-occupancy-detection/notebook






----------------------------------------------------------------------------------------------------------------------------------------------------------
<h2>Installing </h2>

Apache Spark:

    Download Apache Spark from https://www.apache.org/dyn/closer.lua/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
    Go to the directory where spark zip file was downloaded and unpack it:
        tar -zxvf spark-3.5.1-bin-hadoop3.tgz
    Set $JAVA_HOME environmental variable in .bashrc file:
        export JAVA_HOME='/usr/lib/jvm/java-1.8.0-openjdk-amd64'
    In .bashrc file configure other environmental variables for Spark:
        export SPARK_HOME='spark-3.5.1-bin-hadoop3'
        export PATH=$SPARK_HOME:$PATH
        export PATH=$PATH:$SPARK_HOME/bin
        export PYTHONPATH=$SPARK_HOME/python;%SPARK_HOME%\python\lib\py4j-0.10.7-src.zip:%PYTHONPATH%
        export PYSPARK_DRIVER_PYTHON="python" 
        export PYSPARK_PYTHON=python3
        export SPARK_YARN_USER_ENV=PYTHONHASHSE

Apache ZooKeeper

    Manually download the ZooKeeper binaries to the /opt directory:
        cd opt/
        wget https://www-eu.apache.org/dist/zookeeper/zookeeper-3.5.6/apache-zookeeper-3.5.6-bin.tar.gz
    Unpack ZooKeeper repository:
        tar -xvf apache-zookeeper-3.5.6-bin.tar.gz
    Create a symbolic link:
        ln -s apache-zookeeper-3.5.6-bin zookeeper
    Use sample properties:
        cd zookeeper/
        cat conf/zoo_sample.cfg >> conf/zookeeper.properties

Apache Kafka

    Donwload Kafka:
        wget https://www-us.apache.org/dist/kafka/2.3.0/kafka_2.12-2.3.0.tgz
    Unpack Kafka repository:
        tar -xvf kafka_2.12-2.3.0.tgz
    Create a symbolic link:
        ln -s kafka_2.12-2.3.0 kafka

Setting up a multi-broker cluster:

    Create a config file for each of the brokers using sample properties:
        cp config/server.properties config/server-1.properties
        cp config/server.properties config/server-2.properties

    Now edit these new files and set the following properties:

    config/server-1.properties: delete.topic.enable=true broker.id=1 listeners=PLAINTEXT://:9093 log.dirs=/tmp/kafka-logs-1

    config/server-2.properties: delete.topic.enable=true broker.id=2 listeners=PLAINTEXT://:9094 log.dirs=/tmp/kafka-logs-2

Python packages:

Install all packages included in requirements.txt

    Create a virtual environment (conda, virtualenv etc.).
        conda create -n <env_name> python=3.10
    Activate your environment.
        conda activate <env_name>
    Install requirements.
        pip install -r requirements.txt 
    Restart your environment.
        conda deactivate
        conda activate <env_name>

Dependencies

All indispensable JAR files can be found in jar_files directory.
Usage

Start MySQL server:

    service mysql start

Before each run of the application we have to start the ZooKeeper and Kafka brokers:

    Start ZooKeeper:
        cd zookeeper/
        bin/zkServer.sh start conf/zookeeper.properties

    Check if it started correctly:
        bin/zkServer.sh status conf/zookeeper.properties

    Start kafka nodes:
        cd kafka/
        bin/kafka-server-start.sh config/server.properties
        bin/kafka-server-start.sh config/server-1.properties
        bin/kafka-server-start.sh config/server-2.properties

Create Kafka topics if run the application for the first time (list of sample topics can be found in config.py file):

    Create topic:
        bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 3 --partitions 1 --topic topic_name

    List available topics:
        bin/kafka-topics.sh --list --bootstrap-server localhost:9092





1- Create a mysql database by running create_database.py file (it is necessary only with the first use of the application)

2- Run spark_consumer.Py (it have to be launched before data producer).

3- Then we can run producer.py to fetch financial data and send it through Kafka to Pyspark.

4- To make a real-time prediction, the spark_consumer calls predict.py file (the first time we call the training_prediction to train the model, after that we can repeat steps 2-3 but this time time using the existing model to predict the incoming data)






