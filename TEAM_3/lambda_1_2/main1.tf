terraform {
  required_version = ">= 0.13"
}

# ------------------------------------------------------------------------------
# CONFIGURE OUR AWS CONNECTION AND STS ASSUME ROLE
# ------------------------------------------------------------------------------

provider "aws" {
  region = "eu-west-1"

  # assume_role {
  #   profile = ""
  #   role_arn = ""
  #   session_name = ""
  # }
}

# ------------------------------------------------------------------------------
# CONFIGURE REMOTE STATE
# ------------------------------------------------------------------------------

terraform {
  backend "s3" {
    bucket = "team3-delon7-tf-state"
    key    = "terraform.tfstate" # name of state file
    region = "eu-west-1"

    # role_arn = ""
    # session_name = ""
  }
}


################################################################################
# Lambda role
################################################################################

resource "aws_iam_role" "lambda_function_role" {
  name               = "team3-lambda-etl-role-tf"
  assume_role_policy = <<EOF
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
EOF
}

resource "aws_iam_role_policy_attachment" "s3_full_access" {
  role       = aws_iam_role.lambda_function_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_execution_role" {
  role       = aws_iam_role.lambda_function_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "redshift_full_access" {
  role       = aws_iam_role.lambda_function_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRedshiftFullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.lambda_function_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy_attachment" "ssm_read-only_access" {
  role       = aws_iam_role.lambda_function_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"
}

# resource "aws_iam_role_policy_attachment" "sqs_full_access" {
#   role       = aws_iam_role.lambda_function_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
# }

resource "aws_iam_role_policy_attachment" "lambda_sqs_execution" {
  role       = aws_iam_role.lambda_function_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
}

# ################################################################################
# # Lambda functions, layers and invocation
# ################################################################################

# ------------------------------------------------------------------------------
# Lambda 1
# ------------------------------------------------------------------------------

resource "aws_lambda_function" "lambda_1" {
  filename      = "src1.zip"
  function_name = "team3-et-tf"

#   handler       = "src.<python file>.<name of function - must have contnts & events parameter>"
  handler       = "src1/lambda_function.lambda_handler"
  role          =  aws_iam_role.lambda_function_role.arn
  runtime       = "python3.8"
  memory_size   = 512
  timeout       = 60

  source_code_hash = filebase64sha256("src1.zip")

  layers = [
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p38-pandas:4"
  ]

  vpc_config {
    subnet_ids = [
      "subnet-0c74d95d6c6158f23"
    ]

    security_group_ids = ["sg-0a48ea6c50c3d990e"]
  }
}


# resource "aws_lambda_permission" "allow_bucket" {
#   statement_id  = "AllowExecutionFromS3Bucket"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.lambda_l_test.arn
#   principal     = "s3.amazonaws.com"
#   source_arn    = aws_s3_bucket.transactions_bucket.arn
# }


# Invocation
resource "aws_lambda_event_source_mapping" "sqs_lambda1_trigger" {
  event_source_arn = aws_sqs_queue.queue-1.arn
  function_name    = aws_lambda_function.lambda_1.arn
  batch_size = 1
}

# ------------------------------------------------------------------------------
# Lambda 2
# ------------------------------------------------------------------------------

resource "aws_lambda_function" "lambda_2" {
  filename      = "src2.zip"
  function_name = "team3-load-tf"

#   handler       = "src.<python file>.<name of function - must have contnts & events parameter>"
  handler       = "src2/lambda_function.lambda_handler"
  role          =  aws_iam_role.lambda_function_role.arn
  runtime       = "python3.8"
  memory_size   = 512
  timeout       = 300

  source_code_hash = filebase64sha256("src2.zip")

  layers = [
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p38-pandas:4",
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-python38-aws-psycopg2:1"
  ]

  vpc_config {
    subnet_ids = [
      "subnet-0c74d95d6c6158f23"
    ]

    security_group_ids = ["sg-0a48ea6c50c3d990e"]
  }
}


# Invocation
resource "aws_lambda_event_source_mapping" "sqs_lambda2_trigger" {
  event_source_arn = aws_sqs_queue.queue-2.arn
  function_name    = aws_lambda_function.lambda_2.arn
  batch_size = 1
}


# ################################################################################
# # SQS
# ################################################################################

resource "aws_sqs_queue" "queue-1" {
  name = "team3-et-queue-tf"
  visibility_timeout_seconds = 120
  policy = <<EOF
{
  "Version": "2008-10-17",
  "Id": "__default_policy_ID",
  "Statement": [
    {
      "Sid": "__owner_statement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "SQS:*",
      "Resource": "arn:aws:sqs:eu-west-1:370445109106:team3-et-queue-tf",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:*:*:team3-raw-data-tf"
        }
      }
    }
  ]
}
EOF
}

resource "aws_sqs_queue" "queue-2" {
  name = "team3-load-queue-tf"
  visibility_timeout_seconds = 360
  policy = <<EOF
{
  "Version": "2008-10-17",
  "Id": "__default_policy_ID",
  "Statement": [
    {
      "Sid": "__owner_statement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "SQS:*",
      "Resource": "arn:aws:sqs:eu-west-1:370445109106:team3-load-queue-tf",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:*:*:team3-transformed-data-tf"
        }
      }
    }
  ]
}
EOF
}

# ################################################################################
# # S3 buckets and event notifications
# ################################################################################

resource "aws_s3_bucket" "transactions_bucket" {
#   bucket = "team3-store-transactions-data-raw"
    bucket = "team3-raw-data-tf"
}

resource "aws_s3_bucket_notification" "transaction_data_bucket_notification" {
  bucket = aws_s3_bucket.transactions_bucket.id

  queue {
    queue_arn = aws_sqs_queue.queue-1.arn
    events              = ["s3:ObjectCreated:Put"]
    filter_suffix       = ".csv"
  }
}


resource "aws_s3_bucket" "transformed_bucket" {
    bucket = "team3-transformed-data-tf"
}

resource "aws_s3_bucket_notification" "transformed_data_bucket_notification" {
  bucket = aws_s3_bucket.transformed_bucket.id

  queue {
    queue_arn = aws_sqs_queue.queue-2.arn
    events              = ["s3:ObjectCreated:Put"]
    filter_suffix       = ".csv"
  }
}