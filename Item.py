from collections import Counter
import json, os
from os.path import isfile

class Item:
    def __init__(self,brand,name,description,priceBefore,allPricesNow,discount,allImages,url,allSizes,colors,category,originalCategory,subcategory,originalSubcategory,sale,gender):
        self.brand = brand
        self.name = name.replace('"','')
        self.description = description.replace('"','')
        self.priceBefore = priceBefore
        self.allPricesNow = allPricesNow
        self.discount = discount
        self.allImages = allImages
        self.url = url
        self.allSizes = allSizes
        if 'http' in str(colors):
            self.colors = colors
        else:
            col = []
            for c in colors[1:-1].split(','):
                col.append(getColorSrc(c))
            self.colors = col
        self.category = category
        self.originalCategory = originalCategory
        self.subcategory = subcategory
        self.originalSubcategory = originalSubcategory
        self.sale = sale
        self.gender = gender
        self.getCategories()
        self.addToFile()

    def addToFile(self):
        if self.sale:
            sale = '(SALE)'
        else:
            sale = ''
        if not os.path.exists("Output/"):
            os.mkdir("Output/")
        if not os.path.exists("Output/{}{}.json".format(self.brand, sale)):
            open("Output/{}{}.json".format(self.brand, sale),"x",)
            with open("Output/{}{}.json".format(self.brand, sale),"w",encoding="utf8") as f:
                f.write('{"categories":[]}')
        if not os.path.exists("Output/{}{}.json".format(self.category.replace(' ','_'), sale)):
            open("Output/{}{}.json".format(self.category.replace(' ','_'), sale),"x",)
            with open("Output/{}{}.json".format(self.category.replace(' ','_'), sale),"w",encoding="utf8") as f:
                f.write('{"items":[]}')
        data = json.loads(open("Output/{}{}.json".format(self.brand, sale),"r",encoding="utf8").read())
        this = self.__dict__
        isInFile = False
        for category in data['categories']:
            if(this['category']) == category['category']:
                isInFile = True
                break
        if isInFile:
            isInFile = False
            for category in data['categories']:
                if(this['category']) == category['category']:
                    for i in category['items']:
                        if i['url']==this['url']:
                            isInFile = True
                            if not i == this:
                                i['name'] = this['name']
                                i['description'] = this['description']
                                i['priceBefore'] = this['priceBefore']
                                i['allPricesNow'] = this['allPricesNow']
                                i['discount'] = this['discount']
                                i['allImages'] = this['allImages']
                                i['allSizes'] = this['allSizes']
                                i['colors'] = this['colors']
                                i['category'] = this['category']
                                i['originalCategory'] = this['originalCategory']
                                i['subcategory'] = this['subcategory']
                                i['originalSubcategory'] = this['originalSubcategory']
                                i['gender'] = this['gender']
                                i['sale'] = this['sale']
                    if not isInFile:
                        category['items'].append(this)
        else:
            data['categories'].append(json.dumps('{{"category":"{}","items":[{}]}}'.format(this['category'],this)))
        with open("Output/{}{}.json".format(self.brand, sale),"w",encoding="utf8",) as f:
            f.write(str(data).replace("'",'"').replace('\\','').replace('""','').replace('": False,','": false,').replace('": True,','": true,'))
        data = json.loads(open("Output/{}{}.json".format(self.category, sale).replace(' ','_'),"r",encoding="utf8").read())
        isInFile = False
        for item in data['items']:
            if(item['url']) == this['url']:
                isInFile = True
                print(item['name'])
                if not item == this:
                    print('updating...')
                    item['name'] = this['name']
                    item['description'] = this['description']
                    item['priceBefore'] = this['priceBefore']
                    item['allPricesNow'] = this['allPricesNow']
                    item['discount'] = this['discount']
                    item['allImages'] = this['allImages']
                    item['allSizes'] = this['allSizes']
                    item['colors'] = this['colors']
                    item['category'] = this['category']
                    item['originalCategory'] = this['originalCategory']
                    item['subcategory'] = this['subcategory']
                    item['originalSubcategory'] = this['originalSubcategory']
                    item['gender'] = this['gender']
                    item['sale'] = this['sale']
                    break
        if not isInFile:
            data['items'].append(this)
        with open("Output/{}{}.json".format(self.category.replace(' ','_'), sale),"w",encoding="utf8",) as f:
            f.write(str(data).replace("'",'"').replace('\\','').replace('""','').replace('": False,','": false,').replace('": True,','": true,'))

    def getCategories(self):
        cats=[['camisas','camisetas','jerséis','blusas','tops'],
        ['pantalones','jeans','bermudas'],
        ['vestidos','petos'],
        ['faldas','short'],
        ['cazadoras','abrigos','chalecos','sobrecamisas','chaquetas','blazers','cardigans'],
        ['sudaderas','joggers','chándal'],
        ['zapatos','baletas','botas','tacones','sandalias','tennis','tenis','mocasines','oxford','zuecos','spadrillas','shoes','zapatillas','piel'],
        ['bolsos','bandoleras','carteras','mochilas','riñoneras'],
        ['accesorios','gafas','bisutería','cinturones','correas','gorros','fundas','bufandas','medias','decoración']]
        cats2=[['camisa','camiseta','jerséi','jersey','blusa','top','bandeau'],
        ['pantalon','pantalón','jean','jeans','bermuda'],
        ['vestido','peto'],
        ['falda','short'],
        ['cazadora','abrigo','chaleco','sobrecamisa','saco','chubasquero','capa','parka'],
        ['sudadera','jogger','chándal','leggins'],
        ['zapato','baleta','tacon','tacón','sandalia','zapatilla'],
        ['bolso','bandolera','cartera','mochila','riñonera'],
        ['correa','gorro','bufanda','medias','cadena','cadenas','collar','collares','aretes','anillos']]
        categories = ["Camisas y Camisetas","Pantalones y Jeans","Vestidos y Enterizos","Faldas y Shorts","Abrigos y Blazers","Ropa deportiva","Zapatos","Bolsos","Accesorios","Otros"]
        category = ''
        for c in cats:
            for cat in c:
                if cat in self.category.lower():
                    category = categories[cats.index(c)]
        if not category:
            for c in cats2:
                if any(s in c for s in self.name.lower().split(' ')):
                    category = categories[cats2.index(c)]
        if not category:
            category = categories[-1]
        index = categories.index(category)
        if index == 0:
            if any(s in self.name.lower() for s in ['camisa','shirt','blusa','blouse']):
                self.subcategory = 'Camisas'
            elif any(s in self.name.lower() for s in ['camiseta','shirt','t-shirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','polo']):
                self.subcategory = 'Camisetas'
            elif 'top' in self.name.lower():
                self.subcategory = 'Tops'
            elif 'body' in self.name.lower():
                self.subcategory = 'Bodies'
            else:
                self.subcategory = category
        elif index == 1:
            if 'jean' in self.name.lower() or 'jean' in self.category.lower():
                self.subcategory = 'Jeans'
            elif any(s in self.name.lower() for s in ['pantal','trous']):
                self.subcategory = 'Pantalones'
            else:
                self.subcategory = category
        elif index == 2:
            if any(s in self.name.lower() for s in ['vestido','dress']):
                self.subcategory = 'Vestidos'
            elif any(s in self.name.lower() for s in ['enterizo','mono','dungaree','jumpsuit']):
                self.subcategory = 'Enterizos'
            else:
                self.subcategory = category
        elif index == 3:
            if any(s in self.name.lower() for s in ['falda','skirt','minifalda']):
                self.subcategory = 'Faldas'
            elif any(s in self.name.lower() for s in ['short']):
                self.subcategory = 'Shorts'
            else:
                self.subcategory = category
        elif index == 4:
            if any(s in self.name.lower() for s in ['abrigo','chaqueta','gabardina','chaleco','parka']):
                self.subcategory = 'Abrigos'
            elif any(s in self.name.lower() for s in ['blazer','cazadora','sobrecamisa']):
                self.subcategory = 'Blazers'
            else:
                self.subcategory = category
        elif index == 5:
            if any(s in self.name.lower() for s in ['sudadera','jogger']):
                self.subcategory = 'Sudaderas'
            elif any(s in self.name.lower() for s in ['licra','leggy']):
                self.subcategory = 'Licras'
            elif any(s in self.name.lower() for s in ['top']):
                self.subcategory = 'Tops'
            else:
                self.subcategory = category
        elif index == 6:
            if any(s in self.name.lower() for s in ['tenis','tennis']):
                self.subcategory = 'Tenis'
            elif any(s in self.name.lower() for s in ['oxford','clasico']):
                self.subcategory = 'Clásicos'
            elif any(s in self.name.lower() for s in ['sandalia',]):
                self.subcategory = 'Sandalias'
            elif any(s in self.name.lower() for s in ['tacon','tacón']):
                self.subcategory = 'Tacones'
            elif any(s in self.name.lower() for s in ['baleta']):
                self.subcategory = 'Baletas'
            elif any(s in self.name.lower() for s in ['bota','botin','botín']):
                self.subcategory = 'Botas'
            else:
                self.subcategory = category
        else:
            self.subcategory = category
        self.category = category
        if 'sale' in self.subcategory.lower():
            self.subcategory = category

def getColorSrc(colorName):
    colorName = colorName.upper()
    if "BLANCO" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2020/I/0/1/p/2593/560/003/2593560003_3_1_5.jpg?t=1591603662373"
    elif "NEGRO" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2020/I/0/1/p/2520/446/001/2520446001_3_1_5.jpg?t=1578650688731"
    else:
        print(colorName)
        return "Indefinido"
#https://static.e-stradivarius.net/5/photos3/2020/I/0/1/p/3027/005/003/3027005003_3_1_5.jpg?t=1563783037667 Arete
'''
ROJO | 2268/744
ROJO FUERTE | 2636/703
CRUDO
MARINO | 8255/703
KHAKI | 6303/041
AMARILLO CLARO | 2381/347
MULTICOLOR | 2351/300
CREMA | 7484/056
GRIS MEDIO
VERDE
AZUL
ROSA | 3390/003
ÚNICO | 3991/009
MULTICOLOR
AZUL CLARO
FUCSIA
ARENA | 5755/157
VERDE
VERDE AGUA
ROSA CLARO | 5644/329
ROSA CLARO | 5644/325
AZULÓN | 5644/106
VERDE AGUA
'''