terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}


resource "aws_s3_bucket" "bucket" {
  bucket = "bucket-for-rekognition-text-extraction"
}

# Set "BucketOwnerEnforced" which disables ACLs completely and enforces policies only, No need for ACLs, the policy controls all permissions.
resource "aws_s3_bucket_ownership_controls" "ownership_controls" {
  bucket = aws_s3_bucket.bucket.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.bucket.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid = "AllowRekognitionAccess",
        Effect = "Allow",
        Principal = {
          Service = "rekognition.amazonaws.com"
        },
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
        Resource = "arn:aws:s3:::bucket-for-rekognition-text-extraction/*"
      }
    ]
  })
}

output "s3_bucket_name" {
  value = aws_s3_bucket.bucket.bucket
}