import boto3
import logging
import json
from botocore.exceptions import ClientError
from servicio import MailService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context): 
    logger.info("INICIO")
    logger.info(f"EVENT: {str(event)}")

    mail = MailService()
    mail.enviar()
    
    return mail.response.service_response