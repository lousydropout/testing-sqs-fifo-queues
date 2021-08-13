#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from sqs_tests.sqs_tests_stack import SqsTestsStack


app = cdk.App()
SqsTestsStack(
    app,
    "SqsTestsStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)

app.synth()
