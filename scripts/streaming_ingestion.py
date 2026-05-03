from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    IntegerType
)


BASE_DIR = Path(__file__).resolve().parents[1]

input_path = str((BASE_DIR / "data" / "streaming").resolve()).replace("\\", "/")
output_path = str((BASE_DIR / "data" / "bronze" / "streaming_clickstream_events").resolve()).replace("\\", "/")
checkpoint_path = str((BASE_DIR / "data" / "bronze" / "_checkpoints" / "streaming_clickstream").resolve()).replace("\\", "/")


schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("session_id", StringType(), True),
    StructField("event_time", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("category", StringType(), True),
    StructField("device", StringType(), True),
    StructField("country", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("quantity", IntegerType(), True),
])


spark = (
    SparkSession.builder
    .appName("Clickstream Structured Streaming Ingestion")
    .getOrCreate()
)

stream_df = (
    spark.readStream
    .schema(schema)
    .option("maxFilesPerTrigger", 1)
    .json(input_path)
)

bronze_stream_df = (
    stream_df
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("source_file", input_file_name())
)

query = (
    bronze_stream_df.writeStream
    .format("parquet")
    .option("path", output_path)
    .option("checkpointLocation", checkpoint_path)
    .outputMode("append")
    .trigger(availableNow=True)
    .start()
)

query.awaitTermination()

print("Structured streaming ingestion completed.")
print(f"Output path: {output_path}")

spark.stop()