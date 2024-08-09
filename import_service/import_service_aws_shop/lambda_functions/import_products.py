from aws_cdk import (
    aws_lambda as lambda_,
    Stack,
    aws_s3 as s3
)
from constructs import Construct

class ImportProducts(Stack):
    def __init__(self, scope: Construct, construct_id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.lambda_function = lambda_.Function(
            self,
            'ImportProducts',
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset('import_service_aws_shop/lambda_handlers/'),
            handler='import_file_handler.importFileHandler',
                environment={
                'BUCKET_NAME': bucket_name
            }
        )
        bucket = s3.Bucket.from_bucket_name(self, "ImportBucket", bucket_name)
        bucket.grant_read_write(self.lambda_function)