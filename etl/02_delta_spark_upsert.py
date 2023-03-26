import logging
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max, lit

#configuracao de logs da aplicacao
logging.basicConfig(stream=sys.stdout)
logger = logging.getLoggre('datalake_enem_small_upsert')
logger.setLevel(logging.DEBUG)

#cria objeto da spark session
spark = (SparkSession.builder.appName("DeltaExercise")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

logger.info("Importing delta.tables...")

# importa o modulo das tabelas delta; tem de ser depois das linhas do spark acima
from delta.tables import *

logger.info("Produzindo novos dados...")
enemnovo = (
    spark
    .read
    .format("delta")
    .load("s3://datalake-elby-igti-edc-tf/staging-zone/enem/")
)

#define algumas inscricoes (chaves) q serao alteradas; pegar 50 IDs de alunos do arq enem
inscricoes = [
    190001493189,
    190001705261,
    190001421556
]

logger.info("Reduz a 50 casos e faz updates internos no municipio de residencia")
enemnovo = enemnovo.where(enemnovo.NU_INSCRICAO.isin(inscricoes))
enemnovo = enemnovo.wirhColumn("NO_MUNICIPIO_RESIDENCIA", lit("NOVA CIDADE")).withColumn("CO_MUNICIPIO_RESIDENCIA", lit(10000000))

logger.info("Pega os dados do Enem velho na tabela Delta...")
enemvelho = DeltaTable.forPath(spark, "s3://datalake-elby-igti-edc-tf/staging-zone/enem/")

logger.info("Realiza o UPSERT...")
(
    enemvelho.alias("old")
    .merge(enemnovo.alias("new"), "old.NU_INSCRICAO = new.NU_INSCRICAO")
    .whenMatchedUpdateAll()
    .whenNoMatchedInsertAll()
    .execute()
)

logger.info("Atualizacao completa \n\n")

logger.info("Gera manifesto symlink...")
enemvelho.generate("symlink_format_manifest") # isso pq o Athena nao entende arquivo delta

logger.info("Manifesto gerado")
