# conftest.py
import os

def pytest_configure():
    os.environ['BUCKET_NAME'] = 'import-csv-bucket-task5'
