from src.lambda_function.handler import validate_message, connect_dynamodb
import os

def test_validate_message():
    # Test with valid message
    valid_message = {
        "messageText": "This is a valid message."
    }
    validate_message(valid_message)

    # Test with invalid message
    invalid_message = {
        "messageText": "short<10"
    }

    try:
        validate_message(invalid_message)
    except ValueError as e:
        assert str(e) == "Invalid input: 'messageText' must be a string between 10 and 100 characters."

def test_connect_dynamodb():
    # valid_table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    # table = connect_dynamodb(valid_table_name)
    
    invalid_table_name = "photo_table"
    try:
        table = connect_dynamodb(invalid_table_name)
    except ValueError as e:
        assert str(e) == "Failed to connect to DynamoDB."