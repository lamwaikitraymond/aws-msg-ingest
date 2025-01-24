# The Task:
Use cdk in python to create a stack of aws infrastructures:
- msg -> Lambda -> DynamoDB
    1. DynamoDB
        - create a table for storing the msg
    2. Lambda
        - receive input events of msg
        - validate the msg
        - save to DynamoDB
    3. Lambda permissions to write to DynamoDB
    4. API Gateway to invoke the Lambda function
- use pytest to run unit tests for the functions in lambda

# Application of Ingesting Messages using Lambda, and Store to DynamoDB
The solution consists of:
1. **DynamoDB**:
   - Store messages to a table with partition key `messageUUID`.
2. **Lambda**:
   - Process incoming requests, validates the message, and saves it to the DynamoDB.
3. **API Gateway**:
   - Provides an HTTP POST endpoint (`/message`) to submit messages.

## Table of Contents
1. [Deployment](#1-deployment)
2. [Testing](#2-testing-the-result)
3. [Cleaning Up](#3-cleaning-up)

## 1. Deployment
1. Clone repo
   ```bash
      git clone https://github.com/lamwaikitraymond/aws-msg-ingest.git
      cd aws-msg-ingest
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Bootstrap your AWS account environment to CDK:
   ```bash
   cdk bootstrap aws://<account_id>/<region>
   ```
3. Turn on Docker on your local machine
   - As it will create a Docker image for the lambda function during deployment
4. Authenticate Docker with ECR
   ```bash
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<region>.amazonaws.com
   ```
5. Create CloudFormation template (Optional)
   ```bash
   cdk synth
   ```
6. Deploy application
   ```bash
   cdk deploy
   ```
   - Confirm the deployment and note the API Gateway endpoint URL from the output.
      ```
      https://<api-id>.execute-api.<region>.amazonaws.com/prod/message
      ```
## 1a. Error and Handling
### Error:
- You will find the following error during deployment:
   - Cannot build the docker image of the lambda function
   - `Error: The image manifest or layer media type for the source image <image_source> is not supported.`
   - https://github.com/aws/aws-cdk/issues/31548
- root cause:
   - If you are using buildx >= 0.10 specifying target platform does not work since it also creates multi-platform index by default.
### Handling:
   1. Deploy the Lambda function without Docker image
      - In fact, a Docker image is not necessary for Lambda because Lambda is inherently serverless.
      - use `lambda_.Function` instead of `lambda_.DockerImageFunction`
      - But using `DockerImageFunction` is one of the task requirements. Therefore, I didn't go for this way.
   2. set --provenance=false to docker build
      - This way does not work in our case
      - Because we use cdk to auto build the image for us and the cdk doesn't allow passing cli flag in the DockerImageFunction function.
   3. Downgrade Docker Desktop to before v4.34
      - I used this method.

## 2. Testing the result
Once the application is deployed, you can test it using tools like **cURL** or **Postman**.
1. **API Endpoint**:
   - Use the API Gateway endpoint URL provided in the deployment output. The URL will look like:
      ```
      https://<api-id>.execute-api.<region>.amazonaws.com/prod/message
      ```
2. **Sending a POST Request**:
   Send a POST request with a valid JSON payload to the `/message` endpoint:
   ```bash
   curl -X POST \
   -H "Content-Type: application/json" \
   -d '{"messageUUID": "05ceddd6-67e2-429a-a9c3-ea3edf6dbc7e", "messageText": "10 < Test message < 100. It should be valid", "messageDatetime": "2025-01-24 18:04:01"}' \
   https://<api-id>.execute-api.<region>.amazonaws.com/prod/message --ssl-no-revoke
   ```
   - Expected Response:
      ```json
      {
         "message": "Message processed successfully."
      }
      ```
   - Error Response:
      ```json
      {
         "message": "Invalid input: Missing 'messageText'."
      }
      ```
3. **Verify Data in DynamoDB**:
   - Go to the DynamoDB Console

## 3. Cleaning Up
1. Destroy the CDK Stack:
   ```bash
   cdk destroy
   ```
2. Verify Resource Deletion:
   - Go to the AWS Management Console and ensure the DynamoDB table, Lambda function, and API Gateway are deleted.