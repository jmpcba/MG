import logging
import json
from servicio import MailService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context): 
    logger.info("INICIO")
    logger.info(f"EVENT: {str(event)}")

    body = event['body']
    body = json.loads(body)

    mail = MailService()
    mail.enviar(body['mail'], body['presupuestos'])
    
    return mail.response.service_response