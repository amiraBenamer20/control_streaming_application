from pyspark.sql.functions import col, mean, stddev, expr, percentile_approx, count
from pyspark.sql import types
from pyspark.sql import functions as F


# Function to calculate IQR for a column
def calculate_iqr(col_name):
    q1 = percentile_approx(col(col_name), 0.25)
    q3 = percentile_approx(col(col_name), 0.75)
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    return lower_bound, upper_bound

def process_sensor_data(stream, relative_error=0.01):
  
  print("----Process--------")
  df = stream

  # Aggregate to calculate the size of the stream
  size_stream = df\
      .groupBy() \
      .agg(count("*").alias("stream_size"))

  # Start the streaming query to continuously output the stream size
  """query = size_stream \
      .writeStream \
      .outputMode("complete") \
      .format("console") \
      .start()"""
  query = df \
      .writeStream \
      .format("console") \
      .start()
  """
  Removes outliers for each column (Temperature, Light, CO2) using IQR

  Args:
      df: The DataFrame containing sensor data

  Returns:
      A new DataFrame with outliers removed for each column
  """

  
  #analyze_data(stream)

  return  df.writeStream \
  .option("checkpointLocation", "/tmp/spark-checkpoint") \
      .foreachBatch(lambda batch_df: process_batch(batch_df, 0.01)) \
        
               
print("--------------------Process_batch------------------")
def process_batch(batch_df, relative_error):
    columns = ["Temperature","Light", "CO2"]
    for column in columns:
        batch_df = remove_outliers(batch_df,column,relative_error)
    








    return batch_df



def remove_outliers(batch_df,column_name, relative_error):
   
    # Calculate quartiles for Temperature
    q1_temp = batch_df.stat.approxQuantile(column_name, [0.25], relative_error)
    q3_temp = batch_df.stat.approxQuantile(column_name, [0.75], relative_error)

    # Extract quartile values
    q1_temp_value = q1_temp[0]
    q3_temp_value = q3_temp[0]

    # Calculate IQR
    iqr_temp = q3_temp_value - q1_temp_value

    # Define lower and upper bounds
    lower_bound_temp = q1_temp_value - (1.5 * iqr_temp)
    upper_bound_temp = q3_temp_value + (1.5 * iqr_temp)

    # Filter outliers for Temperature
    filtered_df = batch_df.where(col(column_name) >= lower_bound_temp) \
                          .where(col(column_name) <= upper_bound_temp)
    

    
    
    return filtered_df


def analyze_data(batch_df):
     """
    Analyzes and processes a batch of sensor data in a Spark streaming application.

    Args:
        batch_df (Spark DataFrame): The batch of sensor data to analyze and process.
        relative_error (float, optional): Relative error for quartile approximation. Defaults to 0.01.

    Returns:
        Spark DataFrame: The processed DataFrame with outliers removed and additional analysis results.
    """
     # 1. Print the first five rows of the batch
     print("1 - Five rows of dataset:\n", batch_df.head(5))
     print("=" * 80)

     # 2. Descriptive statistics for numerical columns
     print("2 - Statistical info for the numerical columns:\n", batch_df.describe())
     print("=" * 80)

     # 3. Descriptive statistics by occupancy
     print("3 - Statistical info for numerical columns based on occupancy:\n", batch_df.groupby(["Occupancy"]).describe())
     print("=" * 80)




     def fill_missing_data(stream):
        #to do
         return -1