import os
import json
from uuid import uuid4 as uuid
from datetime import datetime
import boto3

sqs = boto3.client("sqs")
num_groups = 7


def create_entry(i: int, j: int) -> dict:
    group_id = str(j % num_groups)
    body = {
        "sk": group_id,
        "timestamp": str(datetime.timestamp(datetime.utcnow())),
    }

    result = {
        "Id": str(i),
        "MessageBody": json.dumps(body),
    }

    if j == -1:  # then it's for standard queue
        return result

    # else, it's for FIFO queue
    return {
        **result,
        "MessageGroupId": group_id,
        "MessageDuplicationId": str(uuid()),
    }


def send_messages(queue: str, is_fifo: bool) -> None:
    for j in range(100):
        __ = sqs.batch_send_message(
            QueueUrl=queue,
            Entries=[create_entry(i, j if is_fifo else -1) for i in range(10)],
        )


def send_to_fifo_queue(event: dict, context) -> None:
    send_messages(queue=os.environ["fifo_queue"], is_fifo=True)


def send_to_std_queue(event: dict, context) -> None:
    send_messages(queue=os.environ["std_queue"], is_fifo=False)
