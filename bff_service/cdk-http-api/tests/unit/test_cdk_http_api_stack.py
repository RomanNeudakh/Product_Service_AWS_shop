import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_http_api.cdk_http_api_stack import CdkHttpApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_http_api/cdk_http_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkHttpApiStack(app, "cdk-http-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })