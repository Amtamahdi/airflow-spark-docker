from pyspark.sql import SparkSession

def run_spark_job():
    spark = SparkSession.builder \
        .appName("TestJob") \
        .getOrCreate()

    # Create a simple DataFrame
    data = [("John", 30), ("Anna", 25), ("Mike", 35)]
    df = spark.createDataFrame(data, ["name", "age"])
    
    # Show the DataFrame
    print("Sample DataFrame:")
    df.show()
    
    # Do a simple aggregation
    print("Average age:")
    df.agg({"age": "avg"}).show()
    
    spark.stop()

if __name__ == "__main__":
    run_spark_job()