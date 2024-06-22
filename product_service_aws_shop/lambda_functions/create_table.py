from aws_cdk import (
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    Stack,
)
from constructs import Construct

class CreateTable(Stack):
    def __init__(self, scope: Construct, construct_id: str, table_name: str, attribute_name: str,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.stocks_table = dynamodb.Table(self, "CreateTable",
            table_name=table_name,
            partition_key=dynamodb.Attribute(
                name=attribute_name,
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY, 
        )