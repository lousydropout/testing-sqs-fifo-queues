import os
import json
from datetime import datetime
from botocore.exceptions import ClientError
import boto3

client = boto3.client("dynamodb")
insert_statement = """INSERT INTO "{table}" VALUE {data};"""


def format_data(record: dict) -> dict:
    """Get data ready to be inserted into DynamoDB table."""
    body = json.loads(record["body"])

    # partition key:
    # add prefix "fifo#" to partition key if message is from FIFO queue
    # else add prefix "std#"
    if record["attributes"].get("MessageGroupId", ""):
        pk = f'fifo#{record["attributes"]["MessageGroupId"]}'
    else:
        pk = f'std#{body["groupId"]}'

    return {
        "pk": pk,
        "sk": body["timestamp"],  # sort key: when the message was created
        "timestamp": str(datetime.timestamp(datetime.utcnow())),
    }


def execute_statement(record: dict) -> None:
    """Execute PartiQL INSERT statement based on."""
    try:
        client.execute_statement(
            Statement=insert_statement.format(
                table=os.environ["table"],
                data=format_data(record),
            )
        )
    except ClientError:
        pass


def lambda_handler(event: dict, context) -> None:
    """INSERT record into DynamoDB table."""
    for record in event.get("Records", []):
        execute_statement(record)
