import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(str(Path(__file__).parents[2]))
from import_service_aws_shop.lambda_handlers.parse_file_handler import parseFileHandler

def test_parse_file_handler_success():
    bucket_name = "test_bucket_name"
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": bucket_name
                    },
                    "object": {
                        "key": "uploaded/test.csv"
                    }
                }
            }
        ]
    }
    mock_get_object = MagicMock()
    mock_get_object.return_value = {
        'Body': MagicMock(read=MagicMock(return_value=b'id,product_name\n30,TestProduct1'))
    }
    context = {}
    with patch('import_service_aws_shop.lambda_handlers.parse_file_handler.s3_client.get_object', mock_get_object), \
         patch('import_service_aws_shop.lambda_handlers.parse_file_handler.s3_client.copy_object') as mock_copy_object, \
         patch('import_service_aws_shop.lambda_handlers.parse_file_handler.s3_client.delete_object') as mock_delete_object:
            parseFileHandler(event, context)

            mock_get_object.assert_called_once_with(
                 Bucket=bucket_name, 
                 Key='uploaded/test.csv'
            )
            mock_copy_object.assert_called_once_with(
                Bucket=bucket_name,
                CopySource={'Bucket': bucket_name, 'Key': 'uploaded/test.csv'},
                Key='parsed/test.csv'
            )
            mock_delete_object.assert_called_once_with(
                Bucket=bucket_name,
                Key='uploaded/test.csv'
            )

def test_parse_file_handler_non_uploaded_folder(caplog):
    bucket_name = "test_bucket_name"
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": bucket_name
                    },
                    "object": {
                        "key": "some_other_folder/test.csv"
                    }
                }
            }
        ]
    }
    context = {}
    parseFileHandler(event, context)
    assert f"File some_other_folder/test.csv is not in the 'uploaded/' folder. Skipping." in caplog.text

