import yaml
import datetime

class Cliente:
    def __init__(self, mail):
        self.mail = mail
    
    def register(self):
        found = False
        clientes = []
        today = datetime.date.today()

        file_path = '/home/juanmanuel.palacios/Documents/personal_repos/MG/backend/registro.yml'
        with open(file_path, 'r') as f:
            clientes = yaml.full_load(f)
        
        for c in clientes:
            if self.mail == c.get('cliente'):
                c['fecha'] = today
                found = True
                break
        
        if not found:
            d = {'cliente': self.mail, 'fecha': today}
            clientes.append(d)
        
        with open(file_path, 'w') as f:
            f.write(yaml.dump(clientes))


cl = Cliente('jmp@gmail.com')
cl.register()
        

