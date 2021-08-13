# Testing SQS queues

## 1. Deploying the stack

You can choose to deploy using either `AWS SAM` or `AWS CDK` (but not both as the way I've named the AWS resources will conflict with each other).

### To deploy using SAM

Note: The following assumes you have the `SAM CLI` installed.

```bash
sam build
sam deploy --guided
```

### To deploy using CDK

Note: The following assumes you have `Node` and `Npm` (Node Package Manager) installed. Also, It's best **_not_** to install AWS CDK and to make use of `npx` instead.

```bash
npx cdk bootstrap
npx cdk deploy
```

## 2. Send messages via SQS Standard and FIFO queues

Two scripts have been written for you, `send_messages_to_std_queue` and `send_messages_to_fifo_queue`.
As you might imagine, the command `./send_messages_to_std_queue` would send messages to the SQS standard queue and
the command `./send_messages_to_fifo_queue` would send messages to the SQS FIFO queue.

Each execution sends `100` messages.

## 3. Run test to see if ordering is preserved.

A script has been written for you, `confirm.py`, that'll query all data from the DynamoDB table and check if ordering is preserved.
To run the script, type in your terminal

```bash
python confirm.py
```
