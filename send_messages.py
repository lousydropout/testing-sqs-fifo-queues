import os
import json
from uuid import uuid4 as uuid
from datetime import datetime
import boto3

sqs = boto3.client("sqs")
num_groups = 7
num_iter = 10


def create_entry(i: int, j: int, is_fifo: bool) -> dict:
    group_id = str(j % num_groups)
    body = {
        "sk": group_id,
        "timestamp": str(datetime.timestamp(datetime.utcnow())),
    }

    result = {
        "Id": str(i),
        "MessageBody": json.dumps(body),
    }

    if not is_fifo:  # then it's for standard queue
        return result

    # else, it's for FIFO queue
    return {
        **result,
        "MessageGroupId": group_id,
        "MessageDeduplicationId": str(uuid()),
    }


def send_messages(queue: str, is_fifo: bool) -> None:
    for j in range(num_iter):
        __ = sqs.send_message_batch(
            QueueUrl=queue,
            Entries=[
                create_entry(i, j * num_iter + i, is_fifo) for i in range(10)
            ],
        )


def send_to_fifo_queue(event: dict, context) -> None:
    send_messages(queue=os.environ["fifo_queue"], is_fifo=True)


def send_to_std_queue(event: dict, context) -> None:
    send_messages(queue=os.environ["std_queue"], is_fifo=False)
