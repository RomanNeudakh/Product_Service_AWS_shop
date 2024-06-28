
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

install dependencies from requirements.txt:
* ```pip install -r requirements.txt```

to deploy this stack to your default AWS account/region:
* ```cdk deploy --all```

to fill the created tables (Product_Cross_Check_table, Stock_Cross_Check_table) with test data, run the script in the root directory:
* ```python fill_tables.py```

In order to run unit tests, install libraries from requirements-dev.txt
* ```pip install -r requirements-dev.txt```

Then run pytest in the root directory:
* ```pytest .```

