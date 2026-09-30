import os
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    from_json,
    lower,
    to_timestamp,
    trim,
    when,
    window,
)
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

ROOT = Path(__file__).resolve().parents[1]
LAKE = ROOT / "data" / "lake"
BRONZE = LAKE / "bronze_stream"
SILVER = LAKE / "silver_stream"
GOLD = LAKE / "gold_stream"
CHECKPOINTS = LAKE / "checkpoints"

for path in (BRONZE, SILVER, GOLD, CHECKPOINTS):
    path.mkdir(parents=True, exist_ok=True)

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
topic = os.getenv("KAFKA_TOPIC", "affirmation-events")

schema = StructType(
    [
        StructField("event_id", StringType()),
        StructField("event_type", StringType()),
        StructField("affirmation_id", IntegerType()),
        StructField("name", StringType()),
        StructField("mood", StringType()),
        StructField("goal", StringType()),
        StructField("category", StringType()),
        StructField("tone", StringType()),
        StructField("source", StringType()),
        StructField("affirmation", StringType()),
        StructField("created_at", StringType()),
    ]
)

spark = (
    SparkSession.builder
    .appName("AffirmationStructuredStreaming")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

kafka_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", bootstrap_servers)
    .option("subscribe", topic)
    .option("startingOffsets", "earliest")
    .load()
)

bronze = (
    kafka_stream
    .selectExpr(
        "CAST(key AS STRING) AS kafka_key",
        "CAST(value AS STRING) AS raw_json",
        "timestamp AS kafka_timestamp",
    )
)

bronze_query = (
    bronze.writeStream
    .format("parquet")
    .option("path", str(BRONZE))
    .option("checkpointLocation", str(CHECKPOINTS / "bronze"))
    .outputMode("append")
    .start()
)

parsed = (
    bronze
    .select(from_json(col("raw_json"), schema).alias("event"))
    .select("event.*")
)

silver = (
    parsed
    .filter(col("event_type") == "affirmation.generated")
    .filter(col("affirmation").isNotNull())
    .filter(trim(col("affirmation")) != "")
    .withColumn("event_time", to_timestamp(col("created_at")))
    .withColumn("category", lower(trim(col("category"))))
    .withColumn(
        "category",
        when(
            col("category").isin(
                "career",
                "confidence",
                "learning",
                "focus",
                "wellbeing",
                "relationships",
                "general",
            ),
            col("category"),
        ).otherwise("general"),
    )
    .withColumn("source", lower(trim(col("source"))))
    .filter(col("event_time").isNotNull())
)

silver_query = (
    silver.writeStream
    .format("parquet")
    .option("path", str(SILVER))
    .option("checkpointLocation", str(CHECKPOINTS / "silver"))
    .outputMode("append")
    .start()
)

gold = (
    silver
    .withWatermark("event_time", "10 minutes")
    .groupBy(
        window(col("event_time"), "5 minutes"),
        col("category"),
        col("source"),
    )
    .agg(count("*").alias("generation_count"))
)

gold_query = (
    gold.writeStream
    .format("parquet")
    .option("path", str(GOLD))
    .option("checkpointLocation", str(CHECKPOINTS / "gold"))
    .outputMode("append")
    .start()
)

spark.streams.awaitAnyTermination()
