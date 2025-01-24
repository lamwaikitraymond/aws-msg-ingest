import aws_cdk as cdk
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_dynamodb as dynamodb
from constructs import Construct
# from aws_cdk import aws_iam as iam

class MsgIngestStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
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

        # # IAM role for the Lambda function is automatically created by the AWS CDK when you define the lambda_.DockerImageFunction
        # lambda_role = iam.Role(
        #     self,
        #     "MsgProcessLambdaRole",
        #     assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        #     description="Custom IAM role for the MsgProcessLambda function",
        # )

        # # Add necessary permissions to the role
        # lambda_role.add_managed_policy(
        #     iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")  # Basic execution role for CloudWatch logging
        # )
        # lambda_role.add_to_policy(
        #     iam.PolicyStatement(
        #         actions=["dynamodb:PutItem"],
        #         resources=[table.table_arn],  # Grant access to the specific DynamoDB table
        #     )
        # )

        # Lambda Function
        lambda_function = lambda_.DockerImageFunction(
            self,
            "MsgProcessLambda",
            code=lambda_.DockerImageCode.from_image_asset("src/lambda_function"),
            environment={
                "DYNAMODB_TABLE_NAME": table.table_name,    # Set the environment variable
            },
            # role=lambda_role,  # Attach the custom IAM role
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

app = cdk.App()
MsgIngestStack(app, "MsgIngestStack")
app.synth()