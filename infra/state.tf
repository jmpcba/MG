terraform {
    backend "s3" {
        bucket = "jmpcba-remote"
        key = "estados/mg/presupuesto.tfstate"
        region = "us-east-1"
    }
}