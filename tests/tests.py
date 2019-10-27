from backend import main

test_body = {
  "body": {
    "mail": "jmpcba@gmail.com",
    "totalPresupuesto": 12,
    "presupuestos": [
      {
        "cantidad": 4,
        "producto": "prod",
        "total": 12,
        "unitario": 3
      }
    ]
  }
}

def test_main():
    main.lambda_handler(test_body, None)

if __name__ == '__main__':
    test_main()