from pyspark.sql.functions import mean, max, min, col, count
from pyspark.sql import SparkSession

spark = (
    SparkSession
    .builder
    .appName("ExerciseSpark")
    .getOrCreate()    
)

# read enem 2019 data
enem = (
    spark
    .read
    .format("csv")
    .option("header", True)
    .option("inferSchema", True)
    .option("delimiter", ";")
    .load("s3://datalake-elby-igti-edc/raw-data/enem/")
)

(
    enem
    .write
    .mode("overwrite")
    .format("parquet")
    #.partitionBy("departamento") # partitionBy("year")   #coluna
    .save("s3://datalake-elby-igti-edc/staging/enem")
)