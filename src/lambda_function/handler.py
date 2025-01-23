import os
import json
import boto3
from datetime import datetime

TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME")

def connect_dynamodb(table_name):
    """
    Connect to dynamodb and return a table
    """
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)
    except:
        raise ValueError("Failed to connect to DynamoDB.")
        
    return table

def validate_message(event):
    """
    Validate input message
    """
    if not isinstance(event, dict):
        raise ValueError("Invalid input: Must be a JSON object.")
    
    if "messageText" not in event:
        raise ValueError("Invalid input: Missing 'messageText'.")
    
    message_text = event["messageText"]
    if not isinstance(message_text, str) or not (10 <= len(message_text) <= 100):
        raise ValueError("Invalid input: 'messageText' must be a string between 10 and 100 characters.")

def process(event, context):
    """
    Process the input event and save it to DynamoDB
    """
    try:
        # Connect to DynamoDB
        table = connect_dynamodb(TABLE_NAME)

        # Validate the input message
        validate_message(event)
        
        # retrive the msg_item
        msg_item = {
            "messageUUID": event.get("messageUUID", ""),
            "messageText": event["messageText"],
            "messageDatetime": event.get("messageDatetime", datetime.utcnow().isoformat())
        }
        
        # Save to DynamoDB
        table.put_item(Item=msg_item)

        # Return success response
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Message processed successfully."})
        }
    except Exception as e:
        # Log error and return failure response
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }