import boto3
from boto3.dynamodb.types import TypeDeserializer
from pprint import pprint

session = boto3.Session(profile_name="cloud", region_name="us-west-2")
client = session.client("dynamodb")
deserializer = TypeDeserializer()

query = """
    SELECT * FROM "sqs-test-table" WHERE BEGINS_WITH("pk", '{qtype}#');
""".strip()


def split_into_groups_and_columns(x: list) -> dict:
    result = {}
    for y in x:
        pk = y["pk"]
        sk = y["sk"]
        ts = y["timestamp"]
        if pk not in result:
            result[pk] = {"sk": [], "ts": []}
        result[pk]["sk"].append(sk)
        result[pk]["ts"].append(ts)
    return result


def is_monotonically_increasing(y):
    if isinstance(y, list):
        return all(x >= y[i - 1] for i, x in enumerate(y) if i > 0)
    if isinstance(y, dict):
        return {k: is_monotonically_increasing(v) for k, v in y.items()}


def main(qtype: str):
    response = client.execute_statement(Statement=query.format(qtype=qtype))
    results = split_into_groups_and_columns(
        [
            {k: deserializer.deserialize(v) for k, v in item.items()}
            for item in response.get("Items", [])
        ]
    )

    print("\n----------")
    print(f"Testing SQS {qtype} queue:")
    print(f"Number of items: {len(response['Items'])}")
    print("----------")

    pprint(is_monotonically_increasing(results))


if __name__ == "__main__":
    main("std")
    main("fifo")
