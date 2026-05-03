from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    countDistinct,
    sum as spark_sum,
    round as spark_round
)


BASE_DIR = Path(__file__).resolve().parents[1]

silver_path = str((BASE_DIR / "data" / "silver" / "clean_clickstream_events").resolve()).replace("\\", "/")
gold_base_path = BASE_DIR / "data" / "gold"


spark = (
    SparkSession.builder
    .appName("Clickstream Gold Analytics")
    .getOrCreate()
)

df = spark.read.parquet(silver_path)

daily_kpis = (
    df.groupBy("event_date")
    .agg(
        count("*").alias("total_events"),
        countDistinct("user_id").alias("active_users"),
        countDistinct("session_id").alias("sessions"),
        spark_round(spark_sum("revenue"), 2).alias("total_revenue")
    )
)

funnel_metrics = (
    df.groupBy("event_type")
    .agg(
        count("*").alias("event_count"),
        countDistinct("user_id").alias("unique_users")
    )
    .orderBy("event_count", ascending=False)
)

product_metrics = (
    df.groupBy("product_id", "category")
    .agg(
        count("*").alias("total_interactions"),
        spark_round(spark_sum("revenue"), 2).alias("revenue")
    )
    .orderBy(col("revenue").desc(), col("total_interactions").desc())
)

daily_kpis.write.mode("overwrite").parquet(str((gold_base_path / "daily_kpis").resolve()).replace("\\", "/"))
funnel_metrics.write.mode("overwrite").parquet(str((gold_base_path / "funnel_metrics").resolve()).replace("\\", "/"))
product_metrics.write.mode("overwrite").parquet(str((gold_base_path / "product_metrics").resolve()).replace("\\", "/"))

print("Gold analytics completed.")
print("Daily KPIs:")
daily_kpis.show(truncate=False)

print("Funnel metrics:")
funnel_metrics.show(truncate=False)

print("Product metrics:")
product_metrics.show(10, truncate=False)

spark.stop()