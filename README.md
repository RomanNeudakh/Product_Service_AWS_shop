# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

 * `cdk ls`                 list all stacks in the app
 * `cdk synth`              emits the synthesized CloudFormation template
 * `cdk deploy --all`       deploy this stack to your default AWS account/region
 * `cdk diff`               compare deployed stack with current state
 * `cdk docs`               open CDK documentation
 * `cdk destroy -all`       delete deployed project from AWS environment

Enjoy!

## cd to requaried service folder.

install dependencies from requirements.txt:
* ```pip install -r requirements.txt```

to deploy this stack to your default AWS account/region:
* ```cdk deploy --all```

In order to run unit tests, install libraries from requirements-dev.txt
* ```pip install -r requirements-dev.txt```

Then run pytest:
* ```pytest .```

## additional information (product_service):

to fill the created tables (Product_Cross_Check_table, Stock_Cross_Check_table) with test data, run the script in the root 
directory:
* ```python fill_tables.py```

## additional information (import_service):

S3 bucket was created manually (bucket_name="import-csv-bucket-task5"). the necessary CORS configurations and Bucket policy were configured