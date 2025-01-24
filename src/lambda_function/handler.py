import os
import json
import boto3
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log INFO level and above

# Get env variables
TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME")

def connect_dynamodb(table_name):
    """
    Connect to dynamodb and return a table
    """
    try:
        logger.info("Connecting to DynamoDB table: %s", table_name)
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)
        logger.info("Successfully connected to DynamoDB table: %s", table_name)
        return table
    except Exception as e:
        logger.error("Failed to connect to DynamoDB: %s", str(e), exc_info=True)
        raise ValueError("Failed to connect to DynamoDB.")

def validate_message(body):
    """
    Validate input message
    """
    logger.info("Validating input message: %s", json.dumps(body))

    # check json format
    if not isinstance(body, dict):
        logger.error("Invalid input: Must be a JSON object.")
        raise ValueError("Invalid input: Must be a JSON object.")
    
    if "messageUUID" not in body:
        logger.error("Invalid input: Missing 'messageUUID'.")
        raise ValueError("Invalid input: Missing 'messageUUID'.")
    
    if "messageText" not in body:
        logger.error("Invalid input: Missing 'messageText'.")
        raise ValueError("Invalid input: Missing 'messageText'.")
    
    if "messageDatetime" not in body:
        logger.error("Invalid input: Missing 'messageDatetime'.")
        raise ValueError("Invalid input: Missing 'messageDatetime'.")
    else:
        # check valid datetime format
        try:
            datetime.strptime(body["messageDatetime"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logger.error("Invalid input: 'messageDatetime' must be in 'YYYY-MM-DD HH:MM:SS' format.")
            raise ValueError("Invalid input: 'messageDatetime' must be in 'YYYY-MM-DD HH:MM:SS' format.")
    
    # check message_text len
    message_text = body["messageText"]
    if not isinstance(message_text, str) or not (10 <= len(message_text) <= 100):
        logger.error("Invalid input: 'messageText' must be a string between 10 and 100 characters.")
        raise ValueError("Invalid input: 'messageText' must be a string between 10 and 100 characters.")
    
    logger.info("Input message validation successful.")

def process(event, context):
    """
    Process the input event and save it to DynamoDB
    """
    logger.info("Processing event: %s", json.dumps(event))
    
    try:
        # Connect to DynamoDB
        table = connect_dynamodb(TABLE_NAME)

        # Extract and parse the body from API Gateway event
        try:
            body = json.loads(event["body"])
        except (KeyError, json.JSONDecodeError):
            logger.error("Invalid input: Missing or invalid JSON body.")
            raise ValueError("Invalid input: Missing or invalid JSON body.")
    
        # Validate the input message
        validate_message(body)
        
        # retrive the msg_item
        msg_item = {
            "messageUUID": body["messageUUID"],
            "messageText": body["messageText"],
            "messageDatetime": body["messageDatetime"]
        }
        
        # Save to DynamoDB
        logger.info("Saving message to DynamoDB: %s", json.dumps(msg_item))
        table.put_item(Item=msg_item)
        logger.info("Message saved successfully to DynamoDB.")

        # Return success response
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Message processed successfully."})
        }
    except Exception as e:
        # Log error and return failure response
        logger.error("Error occurred while processing message: %s", str(e), exc_info=True)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }