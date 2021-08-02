from Item import Item
from Database import Database

def select_db():
    dbs = ['Bershka','Mango','Mercedes Campuzano','Pull & Bear','Stradivarius', 'Zara']
    print('Select db...')
    for d in dbs:
        print(f'{dbs.index(d)}. {d}')
    return Database(dbs[int(input(''))]).db

def from_dict(data):
    return Item(data['brand'],data['name'],data['description'],data['priceBefore'],data['allPricesNow'],data['discount'],data['allImages'],data['url'],data['allSizes'],data['colors'],data['category'],data['originalCategory'],data['subcategory'],data['originalSubcategory'],data['sale'],data['gender'])   

def get_item(id):
    return from_dict(db.get(doc_id=id))

def verify(id):
    item = get_item(id)
    print('Name:', item.name, '\nCategory:', item.category, '\nSubcat:', item.subcategory)
    get_categories(item)
    print('\nNow\nName:', item.name, '\nCategory:', item.category, '\nSubcat:', item.subcategory)

def get_categories(self):
    cats=[
    ['camisas','camisetas','jerséis','blusas','tops'],
    ['pantalones','jeans','bermudas'],
    ['vestidos','petos'],
    ['faldas','shorts','short','bermuda'],
    ['cazadoras','abrigos','chalecos','chaleco','sobrecamisas','chaquetas','blazers','cardigans','cárdigans', 'blasier'],
    ['sudaderas','joggers','chándal','sport','leggings','legging'],
    ['zapatos','baletas','botas','tacones','sandalias','tennis','tenis','mocasines','oxford','zuecos','spadrillas','shoes','zapatillas','piel'],
    ['bolsos','bandoleras','carteras','mochilas','riñoneras'],
    ['accesorios','gafas','bisutería','cinturones','correas','gorros','fundas','bufandas','medias','decoración']]
    cats2=[[['camisa','shirt','blusa','blouse','bluson','blusón','crochet'],['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],['top','bandeau','bralette'],['body', 'bodies']],[['pantalon','pantalón','bermuda','bermudas','capris','trousers'],['jeans','jean','jeggings']],[['vestido','peto','pichi','chaleco','túnica'],['enterizo','kimono','cuerpo','mono']],[['falda','minifalda','skirt','skort'],['shorts','short','bermuda']],[['abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],['sobrecamisa','buzo','blazer']],[['sudadera','jogger','chándal'],['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],['sport', 'sporty']],[['tenis','tennis','deportivas','deportivos'],['oxford','clásico','clasico','zuecos'],['sandalias','trespuntadas'],['baletas','spadrillas','bamba'],['tacones','tacón','zapatos','zapatillas'],['botas','botínes']],[['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],[['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],[[]]]
    categories = ["Camisas y Camisetas","Pantalones y Jeans","Vestidos y Enterizos","Faldas y Shorts","Abrigos y Blazers","Ropa deportiva","Zapatos","Bolsos","Accesorios","Otros"]
    self.category = ''
    for c in cats:
        for cat in c:
            if cat in self.originalCategory.lower():
                index = cats.index(c)
                if index == 0:
                    # If any cardigan in shirts
                    if any(s in self.name.lower() for s in cats[4]):
                        index = 4
                elif index == 1:
                    # If any short in pants
                    if any(s in self.name.lower() for s in cats[3]):
                        index = 3
                    # If any leggin in pants
                    elif any(s in self.name.lower() for s in cats[5]):
                        index = 5
                self.category = categories[index]
    if not self.category:
        for c in cats2:
            for cat in c:
                if any(s in cat for s in self.name.lower().split(' ')) and not self.category:
                    self.category = categories[cats2.index(c)]
    if not self.category:
        self.category = categories[-1]
    self.subcategory = get_subcategory(self, categories.index(self.category), cats2)

def get_subcategory(self, index, cats2):
    sub = self.originalSubcategory.lower()
    name = self.name.lower()
    subs = cats2[index]
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
        elif any(s in name for s in subs[3]):
            return 'Bodies'
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
    return f'{index}_{self.category}'

db = select_db()