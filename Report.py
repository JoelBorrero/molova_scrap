import os, json
path = 'C:/Users/JoelBook/Documents/Molova/Items'
totalItems=0
for file in os.listdir(path):
    if '.json' in file:
        with open('{}/{}'.format(path,file), 'r',encoding='utf8') as f:
            j = json.loads(f.read())
            try:
                brandItems=0
                for c in j['categories']:
                    index2=0
                    for i in c['items']:
                        totalItems+=1
                        index2+=1
                        brandItems+=1
                    #print(index2)
                    print('         ',c['category'],index2)
                print(file,brandItems,'\n')
            except:
                pass
print(totalItems,'productos en total\n')
input('Presiona enter para salir')