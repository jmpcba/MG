import json

class Response:
    """
    Response class. all Service Classes have a response object with a response code and a message
    """
    def __init__(self):
        self._code = 200
        self._body = ''
    
    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, c):
        self._code = c
    
    @property
    def body(self):
        return self._body
    
    @body.setter
    def body(self, b):
        self._body = b
    
    @property
    def service_response(self):
        return self._parse_response()
    
    def _parse_response(self):
        return {
            'headers': {
                'Content-Type': 'application/json', 
                'Access-Control-Allow-Origin': '*' 
                },
            'statusCode': self._code,
            'body': json.dumps(self._body, default=str)
            }

class Service:
    def __init__(self):
        self.response = Response()

class MailService(Service):
    
    def enviar(self):
        # Replace sender@example.com with your "From" address.
        # This address must be verified with Amazon SES.
        SENDER = "Sender Name <jmpcba@gmail.com>"

        # Replace recipient@example.com with a "To" address. If your account 
        # is still in the sandbox, this address must be verified.
        RECIPIENT = "jmpcba@gmail.com"

        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        AWS_REGION = "us-east-1"

        # The subject line for the email.
        SUBJECT = "Amazon SES Test (SDK for Python)"

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                    "This email was sent with Amazon SES using the "
                    "AWS SDK for Python (Boto)."
                    )
                    
        # The HTML body of the email.
        BODY_HTML = """<html>
        <head></head>
        <body>
        <h1>Amazon SES Test (SDK for Python)</h1>
        <p>This email was sent with
            <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
            <a href='https://aws.amazon.com/sdk-for-python/'>
            AWS SDK for Python (Boto)</a>.</p>
        </body>
        </html>
                    """            

        # The character encoding for the email.
        CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        client = boto3.client('ses',region_name=AWS_REGION)

        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        # Display an error if something goes wrong.	
        except Exception as e:
            self.response.code = 403
            self.response.body = e
        else:
            self.response.code = 200