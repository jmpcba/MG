import json
import boto3
import logging
from datetime import date
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def return_code(code, body):
    return {
            'headers': {
                'Content-Type': 'application/json', 
                'Access-Control-Allow-Origin': '*' 
                },
            'statusCode': code,
            'body': json.dumps(body, default=str)
            }

def get_mail_body(presupuestos, monto_total, nota, cliente):
    bucket = 'jmpcba-lambda'
    key = 'mail_template.html'
    s3 = S3(bucket, key)

    table = ''
    today = date.today().strftime("%d-%m-%Y")
    body = s3.get_file_contents()

    for p in presupuestos:
        table += f"<tr><td>{p['producto'].upper()}</td><td>{p['cantidad']}</td><td>${p['unitario']}</td><td>${p['total']}</td></tr>"
    
    body = body.replace('[@TABLA@]', table)
    body = body.replace('[@TOTAL@]', str(monto_total))
    body = body.replace('[@FECHA@]', today)
    body = body.replace('[@NOTA@]', nota)
    body = body.replace('[@CLIENTE@]', cliente)
    
    return body

def lambda_handler(event, context):
    logger.info(event)
    body = event['body']
    body = json.loads(body)
    presupuestos = body['presupuestos']
    cliente = Cliente(body['mail'], body['cliente'])
    monto_total = body['totalPresupuesto']
    nota = body['nota'].upper()
    mail_body = get_mail_body(presupuestos, monto_total, nota, cliente.nombre)
    
    try:
        cliente.send_email(mail_body)
        return return_code(200, 'Mail Enviado')
    
    except Exception as e:
        return return_code(500, e)

class Cliente:
    def __init__(self, mail, nombre):
        self.mail = mail
        self.nombre = nombre
    
    def register(self):
        found = False
        clientes = []
        today = date.today()
        s3 = S3('jmpcba-lambda', 'registro.json')

        logger.info('REGISTRANDO')
        clientes = json.loads(s3.get_file_contents())
        logger.info(f'CLIENTES: {clientes}')
        
        for c in clientes['clientes']:
            if self.mail == c.get('cliente'):
                c['fecha'] = today
                found = True
                logger.info(f'Cliente {self.mail} encontrado, actualizando fecha de contacto')
                break
        
        if not found:
            logger.info('No se encontro el cliente, agregando')
            d = {'cliente': self.mail, 'fecha': today}
            clientes['clientes'].append(d)
        
        logger.info('Guardando cambios en S3')
        s3.set_file_content(json.dumps(clientes, default=str))
    
    def send_email(self, mail_body):
        SENDER = "MG Placas SAS <mgplacassas@gmail.com>"
        AWS_REGION = "us-east-1"
        SUBJECT = "Presupuesto MG Placas"
        CHARSET = "UTF-8"
    
        ses = boto3.client('ses',region_name=AWS_REGION)
        logger.info("Enviando Mail")
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    self.mail,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': mail_body,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': mail_body,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
        
        logger.info("Mail enviado")
        logger.info(response)
        
        try:
            self.register()
        except Exception as e:
            logger.error(e)
        


class S3:
    def __init__(self, bucket, key):
        s3_resource = boto3.resource('s3')
        self.s3_file = s3_resource.Object(bucket, key)
    
    def get_file_contents(self):
        try:
            logger.info("Devolviendo Objeto desde S3")
            return self.s3_file.get()['Body'].read().decode('utf-8')
        except ClientError as e:
            logger.error(e)
            raise

    def set_file_content(self, content):
        try:
            self.s3_file.put(Body=content)
        except ClientError as e:
            logger.error(e)
            raise