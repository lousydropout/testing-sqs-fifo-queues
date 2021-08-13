from aws_cdk import (
    aws_lambda as lambda_,
    aws_lambda_event_sources as eventsources,
    core as cdk,
    aws_sqs as sqs,
    aws_dynamodb as dynamodb,
)

prefix = "sqs-test"


class SqsTestsStack(cdk.Stack):
    def __init__(
        self, scope: cdk.Construct, construct_id: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(
            self,
            "DDBTable",
            table_name=f"{prefix}-table",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=dynamodb.Attribute(
                name="pk", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="sk", type=dynamodb.AttributeType.STRING
            ),
        )

        std_queue = sqs.Queue(
            self, "StdQueue", queue_name=f"{prefix}-std-queue"
        )

        fifo_queue = sqs.Queue(
            self,
            "FifoQueue",
            queue_name=f"{prefix}-fifo-queue.fifo",
            content_based_deduplication=False,
            fifo=True,
        )

        # The code that defines your stack goes here
        handler = lambda_.Function(
            self,
            "HandlerLambda",
            function_name=f"{prefix}-handler",
            code=lambda_.Code.from_asset("./src"),
            handler="handler.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_8,
            environment={"table": table.table_name},
            events=[
                eventsources.SqsEventSource(queue=std_queue),
                eventsources.SqsEventSource(queue=fifo_queue),
            ],
        )
        table.grant_full_access(handler)

        send_to_std = lambda_.Function(
            self,
            "SendMessageStdLambda",
            function_name=f"{prefix}-send-messages-to-std-queue",
            code=lambda_.Code.from_asset("./src"),
            handler="send_messages.send_to_std_queue",
            runtime=lambda_.Runtime.PYTHON_3_8,
            environment={"std_queue": std_queue.queue_url},
        )

        std_queue.grant_send_messages(send_to_std)

        send_to_fifo = lambda_.Function(
            self,
            "SendMessageFifoLambda",
            function_name=f"{prefix}-send-messages-to-fifo-queue",
            code=lambda_.Code.from_asset("./src"),
            handler="send_messages.send_to_fifo_queue",
            runtime=lambda_.Runtime.PYTHON_3_8,
            environment={"fifo_queue": fifo_queue.queue_url},
        )

        fifo_queue.grant_send_messages(send_to_fifo)
