from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    to_timestamp,
    date_format,
    when
)


BASE_DIR = Path(__file__).resolve().parents[1]

bronze_path = str((BASE_DIR / "data" / "bronze" / "clickstream_events").resolve()).replace("\\", "/")
silver_path = str((BASE_DIR / "data" / "silver" / "clean_clickstream_events").resolve()).replace("\\", "/")


spark = (
    SparkSession.builder
    .appName("Clickstream Silver Transformation")
    .getOrCreate()
)

df = spark.read.parquet(bronze_path)

silver_df = (
    df
    .dropDuplicates(["event_id"])
    .withColumn("event_timestamp", to_timestamp(col("event_time")))
    .withColumn("event_date", date_format(col("event_timestamp"), "yyyy-MM-dd"))
    .withColumn(
        "revenue",
        when(col("event_type") == "purchase", col("price") * col("quantity")).otherwise(0)
    )
    .filter(col("event_id").isNotNull())
    .filter(col("user_id").isNotNull())
    .filter(col("session_id").isNotNull())
    .filter(col("event_type").isNotNull())
)

silver_df.write.mode("overwrite").partitionBy("event_date").parquet(silver_path)

print("Silver transformation completed.")
print(f"Rows written: {silver_df.count()}")
print(f"Output path: {silver_path}")

spark.stop()