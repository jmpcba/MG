resource "aws_s3_bucket" "prespuesto_bucket" {
  bucket = "mg-presupuesto-lambda"
  acl    = "public-read"
  policy = <<EOF
  {
    "Version": "2008-10-17",
    "Statement": [
      {
        "Sid": "PublicReadForGetBucketObjects",
        "Effect": "Allow",
        "Principal": {
          "AWS": "*"
        },
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::${var.website_bucket_name}/*"
      }
    ]
  }
  EOF

  website {
    index_document = "index.html"
    error_document = "error.html"

    routing_rules = <<EOF
    [{
        "Condition": {
            "KeyPrefixEquals": "docs/"
        },
        "Redirect": {
            "ReplaceKeyPrefixWith": "documents/"
        }
    }]
    EOF
  }
}