resource "aws_lambda_permission" "MG_lambda_permission" {
  statement_id  = "Allow_data_service_APIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.MG_presupuesto_lambda.function_name}"
  principal     = "apigateway.amazonaws.com"

  # The /*/*/* part allows invocation from any stage, method and resource path
  # within API Gateway REST API.
  source_arn = "${aws_api_gateway_rest_api.MG_restapi.execution_arn}/*/*/*"
}

resource "aws_lambda_function" "MG_presupuesto_lambda" {
  function_name = "mg_presupuesto"
  s3_bucket     = "mg-presupuesto-lambda"
  s3_key        = "presupuesto.zip"
  role          = "${aws_iam_role.MG_presupuesto_lambda_role.arn}"
  runtime       = "python3.6"
  handler       = "main.handler"
}

# IAM
resource "aws_iam_role" "MG_presupuesto_lambda_role" {
    name        = "lambda-vpc-role"
    description = "Allows Lambda functions to call AWS services on your behalf."

    tags = {
          "name" = "mg-presupuesto-lambda-role"
        }

    assume_role_policy = <<POLICY
        {
        "Version": "2012-10-17",
        "Statement": [
            {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
            }
        ]
        }
        POLICY
    }