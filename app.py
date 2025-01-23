from aws_cdk import core as cdk
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as iam

class MsgIngestStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        table = dynamodb.Table(
            self,
            "MsgTable",
            partition_key=dynamodb.Attribute(
                name="messageUUID",
                type=dynamodb.AttributeType.STRING,
            )
        )

        # Lambda Function
        lambda_function = lambda_.DockerImageFunction(
            self,
            "MsgProcessLambda",
            code=lambda_.DockerImageCode.from_image_asset("src/lambda_function"),
            environment={
                "DYNAMODB_TABLE_NAME": table.table_name,    # Set the environment variable
            },
        )

        # Grant Lambda permissions to write to DynamoDB
        table.grant_write_data(lambda_function)

        # API Gateway
        api = apigateway.LambdaRestApi(
            self,
            "MsgProcessAPI",
            handler=lambda_function,
            proxy=False
        )

        # Define resource and endpoint
        message_resource = api.root.add_resource("message")
        message_resource.add_method("POST")     # POST: Submit or create new data.