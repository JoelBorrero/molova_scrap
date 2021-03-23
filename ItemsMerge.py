import Item, os, json
totalItems = 0
percentage = 0
index = 0
path = 'C:/Users/JoelBook/Documents/Molova/Items'
for file in os.listdir(path):
    if '.json' in file:
        with open('{}/{}'.format(path,file), 'r',encoding='utf8') as f:
            j = json.loads(f.read())
            try:
                for c in j['categories']:
                    for i in c['items']:
                        totalItems+=1
            except:
                pass
for file in os.listdir(path):
    if '.json' in file:
        with open('{}/{}'.format(path,file), 'r',encoding='utf8') as f:
            j = json.loads(f.read())
            try:
                for c in j['categories']:
                    for i in c['items'][:100]:
                        Item.Item(i['brand'],i['name'],i['description'],i['priceBefore'],i['allPricesNow'],i['discount'],i['allImages'],i['url'],i['allSizes'],i['colors'],i['category'],i['originalCategory'],i['subcategory'],i['originalSubcategory'],i['sale'],i['gender'])
                        index+=1
                        if not percentage == int(index/totalItems*100):
                            percentage = int(index/totalItems*100)
                            print('{}%      ({} de {})'.format(percentage,index,totalItems))
            except:
                pass