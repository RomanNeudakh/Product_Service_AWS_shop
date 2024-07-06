from aws_cdk import (
    CfnOutput,
    Stack,
    aws_lambda as lambda_,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda_event_sources as event_sources,
    aws_dynamodb as dynamodb_,
    Duration
)
from constructs import Construct

class CreateCatalogBatchProcess(Stack):
    def __init__(self, scope: Construct, id: str, stock_table_name: str, product_table_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        user_imail = 'neudakhroman@gmail.com'
        stock_table = dynamodb_.Table.from_table_name(self, 'StockTable', stock_table_name)
        product_table = dynamodb_.Table.from_table_name(self, 'ProductTable', product_table_name)
        catalog_items_queue = sqs.Queue(
            self, 
            'catalogItemsQueue',
            queue_name='catalogItemsQueueCrossCheck',
            visibility_timeout=Duration.seconds(300)
        )
        create_product_topic = sns.Topic(self, 'createProductTopic')
        create_product_topic.add_subscription(subs.EmailSubscription(user_imail))
        catalog_batch_process = lambda_.Function(
            self, 'catalogBatchProcess',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('product_service_aws_shop/lambda_handlers/'),
            handler='catalog_batch_process_handler.catalogBatchProcessHandler',
            environment={
                'PRODUCT_TABLE': product_table.table_name,
                'STOCK_TABLE': stock_table.table_name,
                'SNS_TOPIC_ARN': create_product_topic.topic_arn
            }
        )
        product_table.grant_read_write_data(catalog_batch_process)
        stock_table.grant_read_write_data(catalog_batch_process)
        create_product_topic.grant_publish(catalog_batch_process)
        catalog_items_queue.grant_consume_messages(catalog_batch_process)
        catalog_batch_process.add_event_source(
            event_sources.SqsEventSource(catalog_items_queue, batch_size=5, max_batching_window=Duration.seconds(10))
        )
        CfnOutput(self, 'CatalogItemsQueueArnOutput',
                  value=catalog_items_queue.queue_arn,
                  export_name='QueueArn')