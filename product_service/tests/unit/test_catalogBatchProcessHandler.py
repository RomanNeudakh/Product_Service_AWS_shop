import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(str(Path(__file__).parents[2]))
from product_service_aws_shop.lambda_handlers.catalog_batch_process_handler import catalogBatchProcessHandler
def test_catalog_batch_process():
    event = {
        'Records': [
            {
                'body': json.dumps({
                    'title': 'test_title_1',
                    'price': 24,
                    'count': 1,
                    'description': 'test_description_1'
                }),
            }
        ]
    }
    product_id = "1234-xxx34-ddd1-ss23" 
    mock_transact_write_item = MagicMock()
    mock_sns = MagicMock()
    mock_uuid = MagicMock()
    mock_uuid.return_value = product_id
    
    product = {
        'id': product_id,
        'title': 'test_title_1',
        'description': 'test_description_1',
        'price': 24.0,
        'count': 1
    }
    context = {}
    with patch('product_service_aws_shop.lambda_handlers.catalog_batch_process_handler.dynamodb.transact_write_items', mock_transact_write_item), \
        patch('product_service_aws_shop.lambda_handlers.catalog_batch_process_handler.uuid.uuid4', mock_uuid), \
        patch('product_service_aws_shop.lambda_handlers.catalog_batch_process_handler.sns.publish', mock_sns):
            res = catalogBatchProcessHandler(event, context)   
            mock_transact_write_item.assert_called_once_with(
                TransactItems=[{
                        'Put': {
                            'TableName': 'Product_Cross_Check_table',
                            'Item':  {
                                'id': {'S': product_id},
                                'title': {'S': 'test_title_1'},
                                'description': {'S': 'test_description_1'},
                                'price': {'N': str(24.0)}
                            }
                        }
                    },
                    {
                        'Put': {
                            'TableName': 'Stock_Cross_Check_table',
                            'Item': {
                                'product_id': {'S': product_id},
                                'count': {'N': str(1)}
                            }
                        }
                    }],
            )
            mock_sns.assert_called_with(
                    TopicArn='test_arn',
                    Message=json.dumps(product),
                    MessageAttributes={
                        'title': {
                            'DataType': 'String',
                            'StringValue': product['title']
                        }
                    }
                )
            
            assert res == {'statusCode': 200, 'body': 'Batch processed successfully'}
def test_catalog_batch_process_invalid_table_name(invalid_table_names):
    event = {
        'Records': [
            {
                'body': json.dumps({
                    'title': 'test_title_1',
                    'price': -24,
                    'count': 1,
                    'description': 'test_description_1'
                }),
            }
        ]
    }
    context = {}
    res = catalogBatchProcessHandler(event, context)
    assert res['statusCode'] == 500
