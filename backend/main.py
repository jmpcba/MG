import json
import boto3
from datetime import date

def return_code(code, body):
    return {
            'headers': {
                'Content-Type': 'application/json', 
                'Access-Control-Allow-Origin': '*' 
                },
            'statusCode': code,
            'body': json.dumps(body, default=str)
            }

def get_mail_body(presupuestos, monto_total):

    s3 = boto3.resource('s3')
    obj = s3.Object('jmpcba-lambda','mail_template.html')
    table = ''
    today = date.today().strftime("%d-%m-%Y")
    body = obj.get()['Body'].read().decode('utf-8') 

    for p in presupuestos:
        table += f"<tr><td>{p['producto']}</td><td>{p['cantidad']}</td><td>{p['unitario']}</td><td>{p['total']}</td></tr>"
    
    body = body.replace('[@TABLA@]', table)
    body = body.replace('[@TOTAL@]', str(monto_total))
    body = body.replace('[@FECHA@]', today)
    
    return body

def lambda_handler(event, context):
    
    body = event['body']
    SENDER = "MG PLacas <jmpcba@gmail.com>"
    AWS_REGION = "us-east-1"
    SUBJECT = "Presupuesto MG Placas"
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    presupuestos = body['presupuestos']
    mail_to = body['mail']
    monto_total = body['totalPresupuesto']
    mail_body = get_mail_body(presupuestos, monto_total)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    mail_to,
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