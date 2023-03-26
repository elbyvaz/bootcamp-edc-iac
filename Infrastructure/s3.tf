resource "aws_s3_bucket" "dl"{
    bucket = "datalake-elby-igti-edc-tf"
    acl = "private"

    tags = {
        NAME = "ELBY",
        IES = "IGTI",
        CURSO = "EDC"
    }

    server_side_encryption_configuration{
        rule{
            apply_server_side_encryption_by_default{
                sse_algorithm = "AES256"
            }
        }
    }
}