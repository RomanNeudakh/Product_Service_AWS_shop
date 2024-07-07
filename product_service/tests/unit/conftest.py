# conftest.py
import os
import pytest

def pytest_configure():
    os.environ['Stock_table_name'] = 'Stock_Cross_Check_table'
    os.environ['Product_table_name'] = 'Product_Cross_Check_table'
    os.environ['PRODUCT_TABLE'] = 'Product_Cross_Check_table'
    os.environ['STOCK_TABLE'] = 'Stock_Cross_Check_table'
    os.environ['SNS_TOPIC_ARN'] = 'test_arn'

@pytest.fixture(scope='function')
def invalid_table_names():
    os.environ['Stock_table_name'] = 'Stock_Cross_Check_table'
    os.environ['Product_table_name'] = 'Product_Cross_Check_table'
    os.environ['PRODUCT_TABLE'] = ''
    os.environ['STOCK_TABLE'] = ''
    os.environ['SNS_TOPIC_ARN'] = 'test_arn'