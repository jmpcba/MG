resource "aws_lambda_function" "MG_lambda" {
  function_name = "mg_presupuesto"
  s3_bucket     = "jmpcba-lambda"
  s3_key        = "presupuesto.zip"
  role          = "${aws_iam_role.MG_presupuesto_lambda_role.arn}"
  runtime       = "python3.7"
  handler       = "main.handler"
}

# IAM
resource "aws_iam_role" "MG_presupuesto_lambda_role" {
    name        = "mg-presupuesto-lambda-role"
    description = "Allows Lambda functions to call AWS services on your behalf."

    tags = {
          "name" = "mg-presupuesto-lambda-role"
        }

    assume_role_policy = <<POLICY
{
"Version":"2012-10-17",
"Statement":[
{
"Action": "sts:AssumeRole",
"Principal":{
"Service":"lambda.amazonaws.com"
},
"Effect":"Allow",
"Sid":""
},
{
"Effect":"Allow",
"Action":[
"ses:SendEmail",
"ses:SendRawEmail"
],
"Resource":"*"
}
]
}
POLICY
}
