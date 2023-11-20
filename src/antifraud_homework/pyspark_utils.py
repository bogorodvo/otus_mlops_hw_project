"""
Functions for data processing with pyspark
"""
import findspark

findspark.init()
findspark.find()
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import date_format, expr, length, col


def clean_data_with_pyspark(s3path_inp: str, s3path_out: str) -> int:
    """
    Basic data cleaning with pyspark
    """
    spark = None

    try:
        # Start SparkSession
        spark = SparkSession.builder.getOrCreate()

        # Define Schema with StringType
        schema = StructType([
            StructField("transaction_id", StringType(), True),
            StructField("tx_datetime", StringType(), True),
            StructField("customer_id", StringType(), True),
            StructField("terminal_id", StringType(), True),
            StructField("tx_amount", StringType(), True),
            StructField("tx_time_seconds", StringType(), True),
            StructField("tx_time_days", StringType(), True),
            StructField("tx_fraud", StringType(), True),
            StructField("tx_fraud_scenario", StringType(), True)
        ])

        # Read .csv from s3 storage
        spark_df = (
            spark.read.format("csv")
            .option("header", "true")
            .option("delimiter", ",")
            .schema(schema)
            .load(s3path_inp)
        )

        # Clean Data
        # Drop Duplicates
        spark_df = spark_df.dropDuplicates()
        # Correct Midnight Error
        spark_df = spark_df.withColumn("tx_datetime", date_format(
            expr("if(substr(tx_datetime, 12) == '24:00:00', \
            from_unixtime(unix_timestamp(substr(tx_datetime, 0, 11) || '00:00:00') + 86400), \
            tx_datetime)"), "yyyy-MM-dd HH:mm:ss"))
        # Correct Seconds
        spark_df = spark_df.withColumn("tx_time_seconds", expr("unix_timestamp(tx_datetime) - unix_timestamp('2019-08-22 00:00:00')"))
        # Correct Days after Midnight Updates
        spark_df = spark_df.withColumn("tx_time_days", expr("tx_time_seconds / 86400").cast(IntegerType()))
        # Drop Raws if customer_id is -999999
        spark_df = spark_df.filter(~(col("customer_id") == -999999))
        # Drop Raws if terminal_id is None, "Err" or length > 4
        spark_df = spark_df.filter(~(col("terminal_id").isNull() | (col("terminal_id") == "Err") | (length(col("terminal_id")) > 4)))

        # Save results with overwrite method
        spark_df.write.parquet(s3path_out, mode="overwrite")
        # logger.error(f"File {s3path_inp} is successfully processed and saved to {s3path_out}.")
        return 0

    except: #Exception as e:
        # logger.error(f"Error message: {e}")
        return 1

    finally:
        # Stop SparkSession
        if spark:
            spark.stop()
