import json, os, pandas as pd

class Item:
    def __init__(self,brand,name,description,priceBefore,allPricesNow,discount,allImages,url,allSizes,colors,category,originalCategory,subcategory,originalSubcategory,sale,gender,crawling=False):
        self.brand = brand
        if not name:
            name = ' '
        self.name = name.replace('"','').replace("'",'')
        if not description:
            description = ' '
        self.description = description.replace('"','').replace("'",'')
        if not priceBefore:
            priceBefore = ' '
        self.priceBefore = priceBefore
        if not isinstance(allPricesNow,list):
            allPricesNow = [allPricesNow]
        self.allPricesNow = allPricesNow
        if not discount:
            discount = ' '
        self.discount = discount
        self.allImages = allImages
        self.url = url
        self.allSizes = allSizes
        if 'http' in str(colors):
            self.colors = colors
        else:
            col = []
            if not crawling:
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
        self.sale = any(toInt(p) < toInt(priceBefore) for p in allPricesNow)
        self.gender = gender
        self.getCategories()
        if crawling:
            self.addToCrawl()
        self.addToFile(crawling=crawling)

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
        cats2=[['camisa','camiseta','jerséi','jersey','blusa','bluson','blusón','top','bandeau','suéter','sueter','sweater','polo','tshirt','t-shirt','crochet'],
        ['pantalon','pantalón','jeans','bermudas','capris','trousers'],
        ['vestido','peto','enterizo','kimono','cuerpo'],
        ['falda','shorts','minifalda','skirt'],
        ['cazadora','abrigo','chaleco','sobrecamisa','saco','chubasquero','capa','parka','buzo','blazer','chaqueta','manguitos','plumíferos','plumiferos','cardigan','cárdigan','rompevientos'],
        ['sudadera','jogger','chándal','leggins','legging'],
        ['zapatos','baletas','tacones','tacón','sandalias','zapatillas','trespuntadas','spadrillas','tenis','botas','zuecos','deportivas','deportivos','botínes','bamba'],
        ['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral'],
        ['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos']]
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
            if any(s in self.name.lower() for s in ['abrigo','chaqueta','gabardina','chaleco','parka','buzo']):
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
            elif any(s in self.name.lower() for s in ['sandalia','trespuntada','spadrilla']):
                self.subcategory = 'Sandalias'
            elif any(s in self.name.lower() for s in ['baleta']):
                self.subcategory = 'Baletas'
            elif any(s in self.name.lower() for s in ['tacon','tacón']):
                self.subcategory = 'Tacones'
            elif any(s in self.name.lower() for s in ['bota','botin','botín']):
                self.subcategory = 'Botas'
            else:
                self.subcategory = category
        else:
            self.subcategory = category
        self.category = category
        if 'sale' in self.subcategory.lower():
            self.subcategory = category

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
        with open("C:/Users/JoelBook/Documents/Molova/Items/COLORS.txt","r",encoding="utf8") as f:
            line=colorName[colorName.index("'")+1:]
            line=line[:line.index("'")]
            if not any(line in l for l in f.readlines()):
                f.close()
                with open("Items/COLORS.txt","a",encoding="utf8") as f:
                    f.write("{}:{}\n".format(line,url))
                f.close()
            else:
                f.close()
        return "https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2545/990/001/2545990001_3_1_5.jpg?t=1613467824691"

def toInt(s):
    s = ''.join(s)
    stf = 0
    for st in s:
        try:
            stf = stf * 10 + int(st)
        except:
            pass
    return stf

def toPrice(s):
    s = str(toInt(s))
    stf = '$ '
    for i in range(len(s)):
        if (len(s)-i)%3==0 and i>0:
            stf=stf+'.'
        stf=stf+s[i]
    return stf

def to_excel(list, path, transpose=True):
    if transpose:
        df = pd.DataFrame(list).T
    else:
        df = pd.DataFrame(list)
    writer = pd.ExcelWriter('{}.xlsx'.format(path), engine='xlsxwriter')
    df.to_excel(writer, sheet_name='welcome', index=False,header=False)
    writer.save()

'''s=''
Item('brand',f"Camisa{s}",
           f"description{s}",
           f"100{s}",
           f"100{s}",
           f"0%{s}",
           [["img","img2"]],
           f"http.url.com",
           f"[s,i,z,e,s]{s}",
           f"color{s}",
           f"Camisetas{s}",
           f"Camisetas{s}",
           f"Camisetas{s}",
           f"Camisetas{s}",
            False,
            "Mujer",
            crawling=True)'''