import json

class JoelDB:
    def __init__(self, name):
        self.name = name
        try:
            with open(f'./Database/{name}.json', 'r') as db:
                self.db = json.loads(db.read())
        except:
            self.db = {'Items': []}
            self.save()

    def save(self):
        with open(f'./Database/{self.name}.json', 'w') as db:
            db.write(json.dumps(self.db))

    def add(self, data):
        if data in self.db['Items']:
            return 'already exist'
        self.db['Items'].append(data)
        self.save()
    
    def get_all(self):
        return self.db['Items']

    def clear(self):
        self.db['Items']=[]