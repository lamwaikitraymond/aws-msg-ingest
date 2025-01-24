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
      git clone <repository-url>
      cd <repository-directory>
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Build Docker image for Lambda
   ```bash
   cd src/lambda_function
   docker build -t msg-process-lambda .
   cd ../../
   ```
4. Create CloudFormation template
   ```bash
   cdk synth
   ```
5. Deploy application
   ```bash
   cdk deploy
   ```
   - Confirm the deployment and note the API Gateway endpoint URL from the output.
      ```
      https://<api-id>.execute-api.<region>.amazonaws.com/prod/message
      ```

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
   -d '{"messageText": "Hello, this is a test message!", "messageUUID": "12345"}' \
   https://<api-id>.execute-api.<region>.amazonaws.com/prod/message
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