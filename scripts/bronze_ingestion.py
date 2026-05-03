from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name


BASE_DIR = Path(__file__).resolve().parents[1]

streaming_dir = BASE_DIR / "data" / "streaming"
input_path = str(streaming_dir.resolve()).replace("\\", "/")
output_path = str((BASE_DIR / "data" / "bronze" / "clickstream_events").resolve()).replace("\\", "/")

print("BASE_DIR:", BASE_DIR)
print("Streaming directory exists:", streaming_dir.exists())
print("Files found:")
for file in streaming_dir.glob("*.json"):
    print(" -", file)

print("Spark input path:", input_path)

spark = (
    SparkSession.builder
    .appName("Clickstream Bronze Ingestion")
    .getOrCreate()
)

df = spark.read.option("multiLine", "false").json(input_path)

bronze_df = (
    df
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("source_file", input_file_name())
)

bronze_df.write.mode("overwrite").parquet(output_path)

print("Bronze ingestion completed.")
print(f"Rows written: {bronze_df.count()}")
print(f"Output path: {output_path}")

spark.stop()