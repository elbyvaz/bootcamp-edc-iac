resource "aws_lambda_function" "executa_emr"{
    filename = "lambda_function_payload.zip"
    function_name = var.lambda_function_name
    role = aws_iam_role.lambda.arn
    handler = "lambda_function.handler"
    memory_size = 128
    timeout = 30

    source_code_hash = filebase64sha256("lambda_function_payload.zip") # criei um .zip fake pra nao dar erro de file nao encontrado

    runtime = "python3.8"

    tags = {
        NAME = "ELBY",
        IES = "IGTI",
        CURSO = "EDC"
    }
}