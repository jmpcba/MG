import json
import boto3
import datetime
from botocore.exceptions import ClientError

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
    
    body = event['body']
    body = json.loads(body)
    SENDER = "MG Placas SAS <mgplacassas@gmail.com>"
    AWS_REGION = "us-east-1"
    SUBJECT = "Presupuesto MG Placas"
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    presupuestos = body['presupuestos']
    cliente = Cliente(body['cliente'], body['mail'])
    monto_total = body['totalPresupuesto']
    nota = body['nota'].upper()
    mail_body = get_mail_body(presupuestos, monto_total, nota, cliente.nombre)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    cliente.mail,
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
        print(response)
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
        today = datetime.date.today()
        s3 = S3('jmpcba', 'registro.json')

        clientes = json.loads(s3.get_file_contents())
        
        for c in clientes['clientes']:
            if self.mail == c.get('cliente'):
                c['fecha'] = today
                found = True
                break
        
        if not found:
            d = {'cliente': self.mail, 'fecha': today}
            clientes['clientes'].append(d)
        
        s3.set_file_content(json.dumps(clientes))

class S3:
    def __init__(self, bucket, key):
        s3_resource = boto3.resource('s3')
        self.s3_file = s3_resource.Object(bucket, key)
    
    def get_file_contents(self):
        try:
            return self.s3_file.get()['Body'].read().decode('utf-8')
        except ClientError:
            return None

    def set_file_content(self, content):
        try:
            self.s3_file.get()['Body'].write(content)
        except ClientError:
            pass