# Tasks:
use cdk in python to create a stack of aws infrastructures:
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