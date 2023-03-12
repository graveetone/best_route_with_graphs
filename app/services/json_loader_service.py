import json

class JsonLoaderService:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        with open(self.filename, encoding='utf-8-sig') as file:
            return json.load(fp=file)
        
    def save(self, obj):
        with open(self.filename, 'w', encoding='utf-8-sig') as file:
            return json.dump(obj, fp=file)