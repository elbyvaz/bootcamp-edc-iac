from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max

#cria objeto da spark session
spark = (SparkSession.builder.appName("DeltaExercise")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

# importa o modulo das tabelas delta; tem de ser depois das linhas do spark acima
from delta.tables import *

# leitura de dados
enem = (
    spark.read.format("csv")
    .option("inferSchema", True)
    .option("header", True)
    .option("delimiter", ";")
    .load("s3://datalake-elby-igti-edc/raw-data/enem/")
)

#escreve a tabela em staging em formato delta
print("Writing delta table...")
(
    enem
    .write
    .mode("overwrite")
    .format("delta")
    #.partitionBy("year")
    .save("s3://datalake-elby-igti-edc-tf/staging-zone/enem/")
)