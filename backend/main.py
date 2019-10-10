import json
import boto3

def return_code(code, body):
    return {
            'headers': {
                'Content-Type': 'application/json', 
                'Access-Control-Allow-Origin': '*' 
                },
            'statusCode': code,
            'body': json.dumps(body, default=str)
            }

def mail_body(presupuestos):
    table = ''
    for p in presupuestos:
        table += f"<tr><td>{p['producto']}</td><td>{p['cantidad']}</td><td>{p['unitario']}</td><td>{p['total']}</td></tr>"
    body = """<html>
        <head></head>
            <body>
            <h1>PRESUPUESTO MG PLACAS Y PLACARES</h1>
            <table>
                [TABLA]
            </table>
        </body>
    </html>"""
    body = body.replace('[TABLA]', table)
    print(body)
    return body

def lambda_handler(event, context):
    
    body = event['body']
    #body = json.loads(body)
    
    
    SENDER = "MG PLacas <jmpcba@gmail.com>"
    AWS_REGION = "us-east-1"
    SUBJECT = "Presupuesto MG Placas Y Placares"
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    presupuestos = body['presupuestos']
    mail = body['mail']
    cuerpo = mail_body(presupuestos)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    mail,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': cuerpo,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': cuerpo,
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