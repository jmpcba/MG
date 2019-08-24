import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context): 
    logger.info("INICIO")
    logger.info(f"EVENT: {str(event)}")

    return event['body']