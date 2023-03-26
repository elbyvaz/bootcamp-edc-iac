# https://www.terraform.io/
# linguagem HCL
# documentacao terraform com s3: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket

# precisa ter o terraform instalado - https://developer.hashicorp.com/terraform/downloads
# como instalar (nao eh obvio): https://jadsonalves.com.br/como-instalar-e-configurar-o-terraform-no-windows/
# fechar o vs code e abrir novamente
# dps de instalado, para rodar: entrar na pasta IaC
# aws configure (caso ainda nao tenha executado)
# terraform (verifica se tudo esta funcionando. Mostra o help)
# terraform init
# terraform fmt (formata o codigo terraform com as indentacoes, alinhamento, etc)
# terraform validate (valida q nao tem erros)
# terraform plan (escreve o plano de execucao de deploy da infra escrita/codificada)
# terraform apply (de fato, cria a estrutura escrita/codificada)
# yes or no
# ...........terraform destroy (destroi tudo o q foi feito - apaga bucket, pastas, files, etc)
# Observacoes: a pasta terraform.state serve para acompanharmos o estado da infra

#         recurso         nome do bucket do terraform (nao da aws)
resource "aws_s3_bucket" "datalake" {

  # parametros de config do recurso escolhido
  bucket = "${var.base_bucket_name}-${var.ambiente}-${var.numero_conta}"
  acl    = "private" # access control list (como vai ser o controle de acesso no s3)
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256" # criptografia default do s3
      }
    }
  } # server_side

  tags = {
    NAME  = "ELBY",
    IES   = "IGTI",
    CURSO = "EDC"
  } # tags

} # resource

resource "aws_s3_bucket_object" "codigo_spark" {
  # bucket = "datalake-elby-igti-edc-tf"
  bucket = aws_s3_bucket.datalake.id # associando o recurso de cima
  key    = "emr-code/pyspark/job_spark_from_tf.py"
  acl    = "private"
  source = "../job_spark.py"          # qual arquivo vamos subir (lembrar q estamos na pasta Iac)
  etag   = filemd5("../job_spark.py") # evitando q toda vez q eu rodar esse codigo o arq seja colocado no s3; soh colocar se tiver mudanca no arq
}                                     # resource

provider "aws" {
  region = "us-east-2"
}