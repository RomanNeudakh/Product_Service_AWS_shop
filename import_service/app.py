#!/usr/bin/env python3

import aws_cdk as cdk

from import_service_aws_shop.import_service_stack import ImportServiceStack


app = cdk.App()
ImportServiceStack(app, "ImportServiceStack")

app.synth()
