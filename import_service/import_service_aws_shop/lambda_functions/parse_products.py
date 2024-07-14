from aws_cdk import (
    aws_lambda as lambda_,
    Stack,
    aws_sqs as sqs,
    aws_s3 as s3,
    Fn
)
from aws_cdk.aws_lambda_event_sources import S3EventSourceV2 
from constructs import Construct

class ParseProducts(Stack):
    def __init__(self, scope: Construct, construct_id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        catalog_items_queue_arn = Fn.import_value('QueueArn')
        catalog_items_queue = sqs.Queue.from_queue_arn(self, 'ImportedCatalogItemsQueue', catalog_items_queue_arn)
        self.lambda_function = lambda_.Function(
            self,
            'ParseProducts',
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset('import_service_aws_shop/lambda_handlers/'),
            handler='parse_file_handler.parseFileHandler',
            environment={
                'BUCKET_NAME': bucket_name,
                'QUEUE_URL': catalog_items_queue.queue_url
            }
        )
        bucket = s3.Bucket.from_bucket_name(self, 'ImportBucket', bucket_name)
        catalog_items_queue.grant_send_messages(self.lambda_function)
        bucket.grant_read_write(self.lambda_function)
        bucket.grant_delete(self.lambda_function)
        self.lambda_function.add_event_source(S3EventSourceV2(bucket,
            events=[s3.EventType.OBJECT_CREATED],
            filters=[s3.NotificationKeyFilter(prefix='uploaded/')]
        ))