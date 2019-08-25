import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context): 
    logger.info("INICIO")
    logger.info(f"EVENT: {str(event)}")
    body = json.loads(event['body'])

    return {
            'statusCode': 200,
            'body': body
            }