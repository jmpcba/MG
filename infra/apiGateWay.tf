# RESTAPI
resource "aws_api_gateway_rest_api" "MG_restapi" {
  name = "MG"
  description = "MG REST service"
}

resource "aws_api_gateway_resource" "api_version_1" {
    rest_api_id = "${aws_api_gateway_rest_api.MG_restapi.id}"
    parent_id   = "${aws_api_gateway_rest_api.MG_restapi.root_resource_id}"
    path_part   = "v1"
}

# DEPLOYMENTS - STAGES
resource "aws_api_gateway_stage" "prod_stage" {
  stage_name    = "${var.prod_stage_name}"
  rest_api_id   = "${aws_api_gateway_rest_api.MG_restapi.id}"
  deployment_id = "${aws_api_gateway_deployment.presupuesto_prod_deployment.id}"
}


resource "aws_api_gateway_deployment" "presupuesto_prod_deployment" {
  depends_on = ["aws_api_gateway_integration.presupuesto_post_integration"]
  rest_api_id = "${aws_api_gateway_rest_api.MG_restapi.id}"
  stage_name  = "prod"
}

resource "aws_api_gateway_stage" "dev_stage" {
  stage_name    = "DEV"
  rest_api_id   = "${aws_api_gateway_rest_api.MG_restapi.id}"
  deployment_id = "${aws_api_gateway_deployment.dev_deployment.id}"
}


resource "aws_api_gateway_deployment" "dev_deployment" {
  depends_on = ["aws_api_gateway_integration.presupuesto_post_integration"]
  rest_api_id = "${aws_api_gateway_rest_api.MG_restapi.id}"
  stage_name  = "DEV"
}

# presupuesto RESOURCES
resource "aws_api_gateway_resource" "presupuesto" {
    rest_api_id = "${aws_api_gateway_rest_api.MG_restapi.id}"
    parent_id   = "${aws_api_gateway_resource.api_version_1.id}"
    path_part   = "presupuesto"
}


resource "aws_api_gateway_method" "presupuesto_post_method" {
    rest_api_id          = "${aws_api_gateway_rest_api.MG_restapi.id}"
    resource_id          = "${aws_api_gateway_resource.presupuesto.id}"
    http_method          = "POST"
    authorization        = "NONE"
}

resource "aws_api_gateway_integration" "presupuesto_post_integration" {
    rest_api_id             = "${aws_api_gateway_rest_api.MG_restapi.id}"
    resource_id             = "${aws_api_gateway_resource.presupuesto.id}"
    http_method             = "${aws_api_gateway_method.presupuesto_post_method.http_method}"
    content_handling        = "CONVERT_TO_TEXT" 
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.MG_presupuesto_lambda.arn}/invocations"
}
