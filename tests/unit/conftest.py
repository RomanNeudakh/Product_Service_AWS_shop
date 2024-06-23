# conftest.py
import os

def pytest_configure():
    os.environ['Stock_table_name'] = 'Stock_Cross_Check_table'
    os.environ['Product_table_name'] = 'Product_Cross_Check_table'
