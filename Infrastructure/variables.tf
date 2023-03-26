variable "base_bucket_name" {
  default = "datalake-elby-igti-edc-tf"
}

variable "ambiente" {
  default = "producao"
}

variable "numero_conta" {
  default = "987035678235"
}

variable "aws_region" {
  default = "us-east-2"
}

variable "lambda_function_name" {
  default = "IGTIexecutaEMR"
}