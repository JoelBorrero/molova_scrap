import json, os

class Item:
    def __init__(self,brand,name,ref,description,priceBefore,allPricesNow,discount,allImages,url,allSizes,colors,category,originalCategory,subcategory,originalSubcategory,sale,gender,crawling=False):
        self.brand = brand
        if not name:
            name = ' '
        self.name = name.replace('"','').replace("'",'')
        self.ref = ref
        if not description:
            description = ' '
        self.description = description.replace('"','').replace("'",'')
        if not priceBefore:
            priceBefore = ' '
        self.priceBefore = toInt(priceBefore)
        self.allPricesNow = allPricesNow
        if not isinstance(self.allPricesNow,list):
            self.allPricesNow = [self.allPricesNow]
        for p in range(len(self.allPricesNow)):
            self.allPricesNow[p] = toInt(self.allPricesNow[p])
        if not discount or toInt(discount)<1:
            self.discount = (1-self.allPricesNow[0]/self.priceBefore)*100
        else:
            self.discount = discount
        self.discount = toInt(self.discount)
        self.allImages = allImages
        try:
            self.url = url[:url.index('.html')+5]
        except:
            self.url = url
        self.allSizes = allSizes
        if 'http' in str(colors):
            self.colors = colors
        else:
            col = []
            for c in str(colors).split(','):
                col.append(getColorSrc(c,url))
            self.colors = col
        if not category:
            category = ' '
        self.category = category
        if not originalCategory:
            originalCategory = category
        self.originalCategory = originalCategory
        if not subcategory:
            subcategory = category
        self.subcategory = subcategory
        if not originalSubcategory:
            originalSubcategory = category
        self.originalSubcategory = originalSubcategory
        self.sale = any(p < toInt(priceBefore) for p in self.allPricesNow)
        self.gender = gender
        self.get_categories()
        # if crawling:
            # self.addToCrawl()
        # self.addToFile(crawling=crawling)

    def addToFile(self,crawling=False):
        if self.sale:
            sale = '(SALE)'
        else:
            sale = ''
        path = 'C:/Users/JoelBook/Documents/Molova/Items/'# if crawling else 'Items/'
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(f"{path}{self.brand}{sale}-{self.gender}.json"):
            open(f"{path}{self.brand}{sale}-{self.gender}.json","x",)
            with open(f"{path}{self.brand}{sale}-{self.gender}.json","w",encoding="utf8") as f:
                f.write('{"categories":[]}')
        if not os.path.exists(f"{path}{self.category.replace(' ','_')}{sale}-{self.gender}.json"):
            open(f"{path}{self.category.replace(' ','_')}{sale}-{self.gender}.json","x",)
            with open(f"{path}{self.category.replace(' ','_')}{sale}-{self.gender}.json","w",encoding="utf8") as f:
                f.write('{"items":[]}')
        data = json.loads(open(f"{path}{self.brand}{sale}-{self.gender}.json","r",encoding="utf8").read())
        this = self.__dict__
        isInFile = False
        for category in data['categories']:
            if(this['category']) == category['category']:
                isInFile = True
                break
        if crawling:
            fields = ['name','description','priceBefore','allPricesNow','discount','allSizes','sale']
        else:
            fields = ['name','description','priceBefore','allPricesNow','discount','allImages','url','allSizes','colors','sale']
        if isInFile:
            isInFile = False
            for category in data['categories']:
                if(this['category']) == category['category']:
                    for i in category['items']:
                        p=0
                        t=0
                        for img in this['allImages']:
                            for imgSub in img:
                                if any(imgSub in imgInd for imgInd in i['allImages']):
                                    p+=1
                                t+=1
                        if t==0:
                            t=1
                        if i['url']==this['url'] or p/t>=.5:
                            isInFile = True
                            if not i == this:
                                for field in fields:
                                    if not i[field] == this[field]:
                                        i[field] = this[field]
                    if not isInFile:
                        category['items'].append(this)
        else:
            data['categories'].append(json.dumps('{{"category":"{}","items":[{}]}}'.format(this['category'],this),ensure_ascii=False))
        with open(f"{path}{self.brand}{sale}-{self.gender}.json","w",encoding="utf8") as f:
            w = str(data).replace("'",'"').replace('\\n','&BR%LN%').replace('\\','').replace('""','').replace('": False,','": false,').replace('": True,','": true,')
            f.write(w.replace('&BR%LN%','\\n'))
        print(f"{path}{self.category.replace(' ','_')}{sale}-{self.gender}.json")
        data = json.loads(open(f"{path}{self.category.replace(' ','_')}{sale}-{self.gender}.json","r",encoding="utf8").read())
        isInFile = False
        for item in data['items']:
            if(item['url']) == this['url']:
                isInFile = True
                if not item == this:
                    for field in fields:
                        if not item[field] == this[field]:
                            item[field] = this[field]
                    break
        if not isInFile:
            #print('Adding {}'.format(this['name']))
            data['items'].append(this)
        with open(f"{path}{self.category.replace(' ','_')}{sale}-{self.gender}.json","w",encoding="utf8",) as f:
            w = str(data).replace("'",'"').replace('\n','&BR%LN%').replace('\\','').replace('""','').replace('": False,','": false,').replace('": True,','": true,')
            f.write(w.replace('&BR%LN%','\n'))

    def addToCrawl(self):
        path = 'C:/Users/JoelBook/Documents/Molova/Items/'
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(f'{path}Crawled.json'):
            open(f'{path}Crawled.json',"x",)
            with open(f'{path}Crawled.json',"w",encoding="utf8") as f:
                f.write('{"brands":[]}')
        data = json.loads(open(f'{path}Crawled.json',"r",encoding="utf8").read())
        this = self.__dict__
        isInFile = False
        for brand in data['brands']:
            if brand['brand'] == this['brand']:
                isInFile = False
                for item in brand['items']:
                    if item['url'] == self.url:
                        isInFile = True
                        break
                if not isInFile:
                    brand['items'].append(this)
                isInFile = True
                break
        if not isInFile:
            data['brands'].append(json.dumps(f'{{"brand":"{this["brand"]}","items":[{this}]""}}',ensure_ascii=False))
        with open(f'{path}Crawled.json',"w",encoding="utf8",) as f:
            w = str(data).replace("'",'"').replace('\\n','&BR%LN%').replace('\\','').replace('""','').replace('": False,','": false,').replace('": True,','": true,')
            f.write(w.replace('&BR%LN%','\\n'))

    def get_categories(self):
        brands_categories={
            'Bershka':[
                ['camisas','camisetas','jerséis','blusas','tops'],
                ['pantalones','jeans','bermudas'],
                ['vestidos','petos'],
                ['faldas','shorts','short'],
                ['cazadoras','abrigos','chalecos','chaleco','sobrecamisas','chaquetas','blazers','cardigans','cárdigans', 'blasier'],
                ['sudaderas','joggers','chándal','sport','legging','leggings'],
                ['zapatos','baletas','botas','tacones','sandalias','tennis','tenis','mocasines','oxford','zuecos','spadrillas','shoes','zapatillas','piel'],
                ['bolsos','bandoleras','carteras','mochilas','riñoneras'],
                ['accesorios','gafas','bisutería','cinturones','correas','gorros','fundas','bufandas','medias','decoración']],
            'Mango':[
                ['camisas','camisetas','jerséis','blusas','tops'],
                ['pantalones','jeans','bermudas'],
                ['vestidos','petos'],
                ['faldas','shorts','short'],
                ['cazadoras','abrigos','chalecos','chaleco','americana','sobrecamisas','chaquetas','blazers','cardigans','cárdigans', 'blasier'],
                ['sudaderas','joggers','chándal','sport','legging','leggings'],
                ['zapatos','baletas','botas','tacones','sandalias','tennis','tenis','mocasines','oxford','zuecos','spadrillas','shoes','zapatillas','piel'],
                ['bolsos','bandoleras','carteras','mochilas','riñoneras'],
                ['accesorios','gafas','bisutería','cinturones','correas','gorros','fundas','bufandas','medias','decoración']],
            'Mercedes Campuzano':[
                ['camisas','camisetas','jerséis','blusas','tops'],
                ['pantalones','jeans','bermudas'],
                ['vestidos','petos'],
                ['faldas','shorts','short'],
                ['cazadoras','abrigos','chalecos','chaleco','sobrecamisas','chaquetas','blazers','cardigans','cárdigans', 'blasier'],
                ['sudaderas','joggers','chándal','sport','legging','leggings'],
                ['zapatos','baletas','botas','tacones','sandalias','tennis','tenis','mocasines','oxford','zuecos','spadrillas','shoes','zapatillas','piel'],
                ['bolsos','bandoleras','carteras','mochilas','riñoneras'],
                ['accesorios','gafas','bisutería','cinturones','correas','gorros','fundas','bufandas','medias','decoración']],
            'Pull & Bear':[
                ['camisas','camisetas','jerséis','blusas','tops'],
                ['pantalones','jeans','bermudas'],
                ['vestidos','petos'],
                ['faldas','shorts','short'],
                ['cazadoras','abrigos','chalecos','chaleco','sobrecamisas','chaquetas','blazers','cardigans','cárdigans', 'blasier'],
                ['sudaderas','joggers','chándal','sport','legging','leggings'],
                ['zapatos','baletas','botas','tacones','sandalias','tennis','tenis','mocasines','oxford','zuecos','spadrillas','shoes','zapatillas','piel'],
                ['bolsos','bandoleras','carteras','mochilas','riñoneras'],
                ['accesorios','gafas','bisutería','cinturones','correas','gorros','fundas','bufandas','medias','decoración']],
            'Stradivarius':[
                ['camisas','camisetas','jerséis','blusas','tops'],
                ['pantalones','jeans','bermudas'],
                ['vestidos','petos'],
                ['faldas','shorts','short'],
                ['jackets','gilet', 'waistcoat','cazadoras','abrigos','chalecos','chaleco','sobrecamisas','chaquetas','blazers','cardigans','cárdigans', 'blasier'],
                ['sudaderas','joggers','chándal','sport','legging','leggings'],
                ['zapatos','baletas','botas','tacones','sandalias','tennis','tenis','mocasines','oxford','zuecos','spadrillas','shoes','zapatillas','piel'],
                ['bags','bolsos','bandoleras','carteras','mochilas','riñoneras'],
                ['accesorios','gafas','bisutería','cinturones','correas','gorros','fundas','bufandas','medias','decoración']],
            'Zara':[
                ['camisas','camisetas','jerséis','blusas','tops'],
                ['pantalones','jeans','bermudas'],
                ['vestidos','petos'],
                ['faldas','shorts','short'],
                ['cazadoras','abrigos','chalecos','chaleco','sobrecamisas','chaquetas','blazers','cardigans','cárdigans', 'blasier'],
                ['sudaderas','joggers','chándal','sport','legging','leggings'],
                ['zapatos','baletas','botas','tacones','sandalias','tennis','tenis','mocasines','oxford','zuecos','spadrillas','shoes','zapatillas','piel'],
                ['bolsos','bandoleras','carteras','mochilas','riñoneras'],
                ['accesorios','gafas','bisutería','cinturones','correas','gorros','fundas','bufandas','medias','decoración']]
            }
        brands_subcategories={
            'Bershka':              [[['camisa','shirt','blusa','blouse','bluson','blusón'],['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],['top','bandeau','bralette'],['body', 'bodies']],[['pantalon','pantalón','bermuda','bermudas','capris','trousers'],['jeans','jean','jeggings']],[['vestido','peto','pichi','chaleco','túnica'],['enterizo','kimono','cuerpo','mono']],[['falda','minifalda','skirt','skort'],['shorts','short','bermuda']],[['abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],['sobrecamisa','buzo','blazer']],[['sudadera','jogger','chándal'],['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],['sport', 'sporty']],[['tenis','tennis','deportivas','deportivos'],['oxford','clásico','clasico','zuecos'],['sandalias','trespuntadas'],['baletas','spadrillas','bamba'],['tacones','tacón','zapatos','zapatillas'],['botas','botínes']],[['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],[['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],[[]]],
            'Mango': [
                [   ['camisa','shirt','blusa','blouse','bluson','blusón'],
                    ['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],
                    ['top','bandeau','bralette'],
                    ['body', 'bodies']],
                [   ['pantalon','pantalón','bermuda','bermudas','capris','trousers'],
                    ['jeans','jean','jeggings']],
                [   ['vestido','peto','pichi','chaleco','túnica'],
                    ['enterizo','kimono','cuerpo','mono']],
                [   ['falda','minifalda','skirt','skort'],
                    ['shorts','short','bermuda']],
                [   ['abrigo','chaqueta','americana','gabardina','chaleco','parka','buzo','capa','cárdigan','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],
                    ['sobrecamisa','buzo','blazer']],
                [   ['sudadera','jogger','chándal'],
                    ['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],
                    ['sport', 'sporty']],
                [   ['tenis','tennis','deportivas','deportivos'],
                    ['oxford','clásico','clasico','zuecos'],
                    ['sandalias','trespuntadas'],
                    ['baletas','spadrillas','bamba'],
                    ['tacones','tacón','zapatos','zapatillas'],
                    ['botas','botínes']],
                [   ['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],
                [   ['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],[[]]],
            'Mercedes Campuzano':   [[['camisa','shirt','blusa','blouse','bluson','blusón'],['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],['top','bandeau','bralette'],['body', 'bodies']],[['pantalon','pantalón','bermuda','bermudas','capris','trousers'],['jeans','jean','jeggings']],[['vestido','peto','pichi','chaleco','túnica'],['enterizo','kimono','cuerpo','mono']],[['falda','minifalda','skirt','skort'],['shorts','short','bermuda']],[['abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],['sobrecamisa','buzo','blazer']],[['sudadera','jogger','chándal'],['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],['sport', 'sporty']],[['tenis','tennis','deportivas','deportivos'],['oxford','clásico','clasico','zuecos'],['sandalias','trespuntadas'],['baletas','spadrillas','bamba'],['tacones','tacón','zapatos','zapatillas'],['botas','botínes']],[['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],[['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],[[]]],
            'Pull & Bear':          [[['camisa','shirt','blusa','blouse','bluson','blusón'],['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],['top','bandeau','bralette'],['body', 'bodies']],[['pantalon','pantalón','bermuda','bermudas','capris','trousers'],['jeans','jean','jeggings']],[['vestido','peto','pichi','chaleco','túnica'],['enterizo','kimono','cuerpo','mono']],[['falda','minifalda','skirt','skort'],['shorts','short','bermuda']],[['abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],['sobrecamisa','buzo','blazer']],[['sudadera','jogger','chándal'],['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],['sport', 'sporty']],[['tenis','tennis','deportivas','deportivos','bamba'],['oxford','clásico','clasico','zuecos'],['sandalias','trespuntadas'],['baletas','spadrillas'],['tacones','tacón','zapatos','zapatillas'],['botas','botínes']],[['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],[['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],[[]]],
            'Stradivarius':         [
                [   ['camisa','shirt','blusa','blouse','bluson','blusón'],
                    ['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],
                    ['top','bandeau','bralette'],
                    ['body', 'bodies','bodysuit']],
                [   ['pantalon','pantalón','bermuda','bermudas','capris','trousers'],
                    ['jeans','jean','jeggings']],
                [   ['vestido','peto','pichi','chaleco','túnica'],
                    ['enterizo','kimono','cuerpo','mono']],
                [   ['falda','minifalda','skirt','skort'],
                    ['shorts','short','bermuda']],
                [   ['gilet','waistcoat','jacket','abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],
                    ['sobrecamisa','buzo','blazer']],
                [   ['sudadera','jogger','chándal'],
                    ['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],
                    ['sport', 'sporty']],
                [   ['tenis','tennis','deportivas','deportivos'],
                    ['oxford','clásico','clasico','zuecos'],
                    ['sandalias','trespuntadas'],
                    ['baletas','spadrillas','bamba'],
                    ['tacones','tacón','zapatos','zapatillas'],
                    ['botas','botínes','botines']],
                [   ['bag','bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],
                [   ['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],[[]]],
            'Zara':                 [[['camisa','shirt','blusa','blouse','bluson','blusón'],['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],['top','bandeau','bralette'],['body', 'bodies']],[['pantalon','pantalón','bermuda','bermudas','capris','trousers'],['jeans','jean','jeggings']],[['vestido','peto','pichi','chaleco','túnica'],['enterizo','kimono','cuerpo','mono']],[['falda','minifalda','skirt','skort'],['shorts','short','bermuda']],[['abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],['sobrecamisa','buzo','blazer']],[['sudadera','jogger','chándal'],['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],['sport', 'sporty']],[['tenis','tennis','deportivas','deportivos'],['oxford','clásico','clasico','zuecos'],['sandalias','trespuntadas'],['baletas','spadrillas','bamba'],['tacones','tacón','zapatos','zapatillas'],['botas','botínes']],[['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],[['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],[[]]],
        }
        categories = ["Camisas y Camisetas","Pantalones y Jeans","Vestidos y Enterizos","Faldas y Shorts","Abrigos y Blazers","Ropa deportiva","Zapatos","Bolsos","Accesorios","Otros"]
        self.category = ''
        categories_list = brands_categories[self.brand]
        subcategories_list = brands_subcategories[self.brand]
        for c in categories_list:
            for cat in c:
                if cat in self.originalCategory.lower():
                    index = categories_list.index(c)
                    if index == 0:
                        # If any cardigan in shirts
                        if any(s in self.name.lower() for s in categories_list[4]):
                            index = 4
                    elif index == 1:
                        # If any short in pants
                        if any(s in self.name.lower() for s in categories_list[3]):
                            index = 3
                        # If any leggin in pants
                        elif any(s in self.name.lower() for s in categories_list[5]):
                            index = 5
                    self.category = categories[index]
        if not self.category:
            for c in subcategories_list:
                for cat in c:
                    if any(s in cat for s in self.name.lower().split(' ')) and not self.category:
                        self.category = categories[subcategories_list.index(c)]
        if not self.category:
            self.category = categories[-1]
        self.subcategory = self.get_subcategory(categories.index(self.category), subcategories_list)

    def get_subcategory(self, index, subcategories_list):
        sub = self.originalSubcategory.lower()
        name = self.name.lower()
        subs = subcategories_list[index] if index <7 else ''
        if index == 0:
            if any(s in sub for s in subs[0]) and not any(s in sub for s in subs[1]+subs[2]+subs[3]):
                return 'Camisas'
            elif any(s in sub for s in subs[1]) and not any(s in sub for s in subs[2]+subs[3]):
                return 'Camisetas'
            elif any(s in sub for s in subs[2]) and not any(s in sub for s in subs[3]):
                return 'Tops'
            elif any(s in sub for s in subs[3]):
                return 'Bodies'
            elif any(s in name for s in subs[0]):
                return 'Camisas'
            elif any(s in name for s in subs[1]):
                return 'Camisetas'
            elif any(s in name for s in subs[2]):
                return 'Tops'
        elif index == 1:
            if any(s in sub for s in subs[0]) and not any(s in sub for s in subs[1]):
                return 'Pantalones'
            elif any(s in sub for s in subs[1]):
                return 'Jeans'
            elif any(s in name for s in subs[0]):
                return 'Pantalones'
            elif any(s in name for s in subs[1]):
                return 'Jeans'
        elif index == 2:
            if any(s in sub for s in subs[0]) and not any(s in sub for s in subs[1]):
                return 'Vestidos'
            elif any(s in sub for s in subs[1]):
                return 'Enterizos'
            elif any(s in name for s in subs[0]):
                    return 'Vestidos'
            elif any(s in name for s in subs[1]):
                return 'Enterizos'
        elif index == 3:
            if any(s in sub for s in subs[0]) and not any(s in sub for s in subs[1]):
                return 'Faldas'
            elif any(s in sub for s in subs[1]):
                return 'Shorts'
            elif any(s in name for s in subs[0]):
                return 'Faldas'
            elif any(s in name for s in subs[1]):
                return 'Shorts'
        elif index == 4:
            if any(s in sub for s in subs[0]) and not any(s in sub for s in subs[1]):
                return 'Abrigos'
            elif any(s in sub for s in subs[1]):
                return 'Blazers'
            elif any(s in name for s in subs[0]):
                return 'Abrigos'
            elif any(s in name for s in subs[1]):
                return 'Blazers'
        elif index == 5:
            if any(s in sub for s in subs[0]) and not any(s in sub for s in subs[1]+subs[2]):
                return 'Sudaderas'
            elif any(s in sub for s in subs[1]) and not any(s in sub for s in subs[2]):
                return 'Licras'
            elif any(s in sub for s in subs[2]):
                return 'Tops'
            elif any(s in name for s in subs[0]):
                return 'Sudaderas'
            elif any(s in name for s in subs[1]):
                return 'Licras'
            elif any(s in name for s in subs[2]):
                return 'Tops'
        elif index == 6:
            if any(s in sub+name for s in subs[0]) :
                return 'Tenis'
            elif any(s in sub+name for s in subs[1]):
                return 'Clásicos'
            elif any(s in sub+name for s in subs[2]):
                return 'Sandalias'
            elif any(s in sub+name for s in subs[3]):
                return 'Baletas'
            elif any(s in sub+name for s in subs[4]):
                return 'Tacones'
            elif any(s in sub+name for s in subs[5]):
                return 'Botas'
        return f'_{index}_{self.category}'
        

def getColorSrc(colorName,url):
    colorName = colorName.lower()
    if "blanco" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2020/I/0/1/p/2593/560/003/2593560003_3_1_5.jpg?t=1591603662373"
    elif "negro" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2020/I/0/1/p/2520/446/001/2520446001_3_1_5.jpg?t=1578650688731"
    elif any(c in colorName for c in ['khaki oscuro']):
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/1809/189/550/1809188550_3_1_5.jpg?t=1584638546032"
    elif any(c in colorName for c in ['crudo','natural']):
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/5806/616/004/5806616004_3_1_5.jpg?t=1606239230009"
    elif any(c in colorName for c in ['verde caqui','verdoso']):
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2532/688/550/2532688550_3_1_5.jpg?t=1612276973740"
    elif any(c in colorName for c in ['gris claro','gris vigor']):
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/5800/128/201/5800128201_3_1_5.jpg?t=1614169933321"
    elif "marrón" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2020/I/0/1/p/5005/476/415/5005476415_3_1_5.jpg?t=1602670087866"
    elif "azul claro" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/5800/128/040/5800128040_3_1_5.jpg?t=1614169933139"
    elif any(c in colorName for c in ['camel','tostao']):
        return "https://static.e-stradivarius.net/5/photos3/2021/V/1/1/p/9200/770/102/02/9200770102_3_1_5.jpg?t=1614267634783"
    elif "rosa" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2617/490/146/2617490146_3_1_5.jpg?t=1613480445018"
    elif "fucsia" in colorName:
        return "https://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/GEF/ES-CO/Imagenes/Swatches/swatches_genericos/Rojo-3002.png"
    elif "verde claro" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2530/151/505/2530151505_3_1_5.jpg?t=1611059016110"
    elif any(c in colorName for c in ['verde','131']):
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2545/860/508/2545860508_3_1_5.jpg?t=1612868332925"
    elif "celeste" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2530/151/045/2530151045_3_1_5.jpg?t=1611052287184"
    elif "dorado" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/0783/006/300/0783006300_3_1_5.jpg?t=1607013413999"
    elif "lila" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2545/860/601/2545860601_3_1_5.jpg?t=1612868333047"
    elif "beige" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2020/I/0/1/p/6540/888/430/6540888430_3_1_5.jpg?t=1602063024098"
    elif "gris" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/8061/294/210/8061294210_3_1_5.jpg?t=1613663030327"
    elif "rojo" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/5902/235/101/5902235101_3_1_5.jpg?t=1599738732391"
    elif "azul" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2502/423/045/2502423045_3_1_5.jpg?t=1606757897269"
    elif any(c in colorName for c in ['amarillo','mostaza']):
        return "https://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/2020/GEF/ES-CO/Imagenes/Swatches/swatches_genericos/Amarillo-11048.png"
    elif "naranja" in colorName:
        return "https://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/2020/GEF/ES-CO/Imagenes/Swatches/swatches_genericos/Naranja-38836.png"
    elif "lima" in colorName:
        return "https://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/GEF/ES-CO/Imagenes/Swatches/swatches_genericos/VERDE_NEON_6654.PNG"
    elif "verde" in colorName:
        return "https://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/GEF/ES-CO/Imagenes/Swatches/swatches_genericos/Verde-15849.png"
    elif "az" in colorName:
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2512/446/010/2512446010_3_1_5.jpg?t=1606152337393"
    else:
    #     try:
    #         with open("C:/Users/JoelBook/Documents/Molova/Items/COLORS.txt","r",encoding="utf8") as f:
    #             line=colorName[colorName.index("'")+1:]
    #             line=line[:line.index("'")]
    #             if not any(line in l for l in f.readlines()):
    #                 f.close()
    #                 with open("Items/COLORS.txt","a",encoding="utf8") as f:
    #                     f.write("{}:{}\n".format(line,url))
    #                 f.close()
    #             else:
    #                 f.close()
    #     except:
    #         pass
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2545/990/001/2545990001_3_1_5.jpg?t=1613467824691"

def toInt(s):
    if type(s) is float:
        s = int(s)  
    if not type(s) is int:
        stf = 0
        s = ''.join(str(s))
        for st in s:
            try:
                stf = stf * 10 + int(st)
            except:
                pass
        return stf
    else:
        return s

def from_dict(data):
    return Item(data['brand'],data['name'],data['description'],data['priceBefore'],data['allPricesNow'],data['discount'],data['allImages'],data['url'],data['allSizes'],data['colors'],data['category'],data['originalCategory'],data['subcategory'],data['originalSubcategory'],data['sale'],data['gender'])   