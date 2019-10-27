import sys
from os import environ, path
import main

test_body = {
  "body": """{
    "mail": "jmpcba@gmail.com",
    "totalPresupuesto": 12,
    "cliente": "manuel",
    "nota": "sin notas",
    "presupuestos": [
      {
        "cantidad": 4,
        "producto": "prod",
        "total": 12,
        "unitario": 3
      }
    ]
  }"""
}

def test_main():
    main.lambda_handler(test_body, None)

if __name__ == '__main__':
    environ['AWS_PROFILE'] = 'personal'
    test_main()