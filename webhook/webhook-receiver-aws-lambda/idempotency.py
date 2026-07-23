"""Prevent repeated Jira webhook processing through DynamoDB."""

import os
import time

import boto3
from botocore.exceptions import ClientError


idempotency_table = boto3.resource("dynamodb").Table(
    os.environ["IDEMPOTENCY_TABLE"]
)


def register_webhook(webhook_id):
    """Register a webhook atomically and return False for a duplicate."""
    now = int(time.time())
    try:
        idempotency_table.put_item(
            Item={
                "webhook_id": webhook_id,
                "created_at": now,
                "expires_at": now + 7 * 24 * 60 * 60,
            },
            ConditionExpression="attribute_not_exists(webhook_id)",
        )
        return True
    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "ConditionalCheckFailedException":
            return False
        raise


def forget_webhook(webhook_id):
    """Remove a webhook registration after processing has failed."""
    idempotency_table.delete_item(
        Key={
            "webhook_id": webhook_id,
        },
    )
