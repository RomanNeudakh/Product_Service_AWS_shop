import aws_cdk as cdk
from cdk_http_api.cdk_http_api_stack import httpApi
app = cdk.App()
httpApi(app, "httpApi")
app.synth()
