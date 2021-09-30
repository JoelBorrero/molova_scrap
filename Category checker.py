import ast
from tinydb import Query
from Item import Item
from Database import Database

def select_db():
    dbs = ['Bershka','Mango','Mercedes Campuzano','Pull & Bear','Stradivarius', 'Zara']
    print('Select db...')
    for d in dbs:
        print(f'{dbs.index(d)}. {d}')
    return Database(dbs[int(input(''))]).db

def verify(id):
    item = db.get(doc_id=id)
    print('Before\nName:', item['name'], '\nCategory:', item['category'], '\nSubcat:', item['subcategory'])
    item = Item(item['brand'],item['name'],'ref',item['description'],item['priceBefore'],item['allPricesNow'],item['discount'],item['allImages'],item['url'],item['allSizes'],item['colors'],item['category'],item['originalCategory'],item['subcategory'],item['originalSubcategory'],item['gender'])   
    print('\nNow\nName:', item.name, '\nCategory:', item.category, '\nSubcat:', item.subcategory)
    db.update(item.__dict__, Query().url == item.url)

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
                ['cazadoras','abrigos','chalecos','chaleco','sobrecamisas','chaquetas','blazers','cardigans','cárdigans', 'blasier'],
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
                ['cazadoras','abrigos','chalecos','chaleco','sobrecamisas','chaquetas','blazers','cardigans','cárdigans', 'blasier'],
                ['sudaderas','joggers','chándal','sport','legging','leggings'],
                ['zapatos','baletas','botas','tacones','sandalias','tennis','tenis','mocasines','oxford','zuecos','spadrillas','shoes','zapatillas','piel'],
                ['bolsos','bandoleras','carteras','mochilas','riñoneras'],
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
            'Bershka': [[['camisa','shirt','blusa','blouse','bluson','blusón'],['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],['top','bandeau','bralette'],['body', 'bodies']],
            [['pantalon','pantalón','bermuda','bermudas','capris','trousers'],['jeans','jean','jeggings']],
            [['vestido','peto','pichi','chaleco','túnica'],['enterizo','kimono','cuerpo','mono']],
            [['falda','minifalda','skirt','skort'],['shorts','short','bermuda']],
            [['abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],['sobrecamisa','buzo','blazer']],
            [['sudadera','jogger','chándal'],['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],['sport', 'sporty']],
            [['tenis','tennis','deportivas','deportivos'],['oxford','clásico','clasico','zuecos'],['sandalias','trespuntadas'],['baletas','spadrillas','bamba'],['tacones','tacón','zapatos','zapatillas'],['botas','botínes']],
            [['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],
            [['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],
            [[]]],

            'Mango':                [[['camisa','shirt','blusa','blouse','bluson','blusón'],['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],['top','bandeau','bralette'],['body', 'bodies']],
            [['pantalon','pantalón','bermuda','bermudas','capris','trousers'],['jeans','jean','jeggings']],
            [['vestido','peto','pichi','chaleco','túnica'],['enterizo','kimono','cuerpo','mono']],
            [['falda','minifalda','skirt','skort'],['shorts','short','bermuda']],
            [['abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],['sobrecamisa','buzo','blazer']],
            [['sudadera','jogger','chándal'],['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],['sport', 'sporty']],
            [['tenis','tennis','deportivas','deportivos'],['oxford','clásico','clasico','zuecos'],['sandalias','trespuntadas'],['baletas','spadrillas','bamba'],['tacones','tacón','zapatos','zapatillas'],['botas','botínes']],
            [['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],
            [['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],
            [[]]],

            'Mercedes Campuzano':   [[['camisa','shirt','blusa','blouse','bluson','blusón'],['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],['top','bandeau','bralette'],['body', 'bodies']],
            [['pantalon','pantalón','bermuda','bermudas','capris','trousers'],['jeans','jean','jeggings']],
            [['vestido','peto','pichi','chaleco','túnica'],['enterizo','kimono','cuerpo','mono']],
            [['falda','minifalda','skirt','skort'],['shorts','short','bermuda']],
            [['abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],['sobrecamisa','buzo','blazer']],
            [['sudadera','jogger','chándal'],['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],['sport', 'sporty']],
            [['tenis','tennis','deportivas','deportivos'],['oxford','clásico','clasico','zuecos'],['sandalias','trespuntadas'],['baletas','spadrillas','bamba'],['tacones','tacón','zapatos','zapatillas'],['botas','botínes']],
            [['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],
            [['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],
            [[]]],

            'Pull & Bear':          [[['camisa','shirt','blusa','blouse','bluson','blusón'],['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],['top','bandeau','bralette'],['body', 'bodies']],
            [['pantalon','pantalón','bermuda','bermudas','capris','trousers'],['jeans','jean','jeggings']],
            [['vestido','peto','pichi','chaleco','túnica'],['enterizo','kimono','cuerpo','mono']],
            [['falda','minifalda','skirt','skort'],['shorts','short','bermuda']],
            [['abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],['sobrecamisa','buzo','blazer']],
            [['sudadera','jogger','chándal'],['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],['sport', 'sporty']],
            [['tenis','tennis','deportivas','deportivos','bamba'],['oxford','clásico','clasico','zuecos'],['sandalias','trespuntadas'],['baletas','spadrillas'],['tacones','tacón','zapatos','zapatillas'],['botas','botínes']],
            [['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],
            [['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],
            [[]]],

            'Stradivarius':         [[['camisa','shirt','blusa','blouse','bluson','blusón'],['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],['top','bandeau','bralette'],['body', 'bodies']],
            [['pantalon','pantalón','bermuda','bermudas','capris','trousers'],['jeans','jean','jeggings']],
            [['vestido','peto','pichi','chaleco','túnica'],['enterizo','kimono','cuerpo','mono']],
            [['falda','minifalda','skirt','skort'],['shorts','short','bermuda']],
            [['abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],['sobrecamisa','buzo','blazer']],
            [['sudadera','jogger','chándal'],['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],['sport', 'sporty']],
            [['tenis','tennis','deportivas','deportivos'],['oxford','clásico','clasico','zuecos'],['sandalias','trespuntadas'],['baletas','spadrillas','bamba'],['tacones','tacón','zapatos','zapatillas'],['botas','botínes']],
            [['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],
            [['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras']],
            [[]]],
            'Zara':                 [
                [['camisa','shirt','blusa','blouse','bluson','blusón'],['camiseta','shirt','t-shirt','tshirt','basic','básica','basica','estampado','estampada','license','licencia','manga','jacket','jersey','jersei','jerséi','polo','suéter','sueter','sweater'],['top','bandeau','bralette','cuerpo','bustier','crop'],['body', 'bodies']],
                [['pantalon','pantalón','bermuda','bermudas','capris','trousers','jogger'],['jeans','jean','jeggings']],
                [['vestido','peto','pichi','chaleco','túnica','tunica'],['enterizo','kimono','cuerpo','mono','largo']],
                [['falda','minifalda','skirt','skort'],['shorts','short','bermuda']],
                [['abrigo','chaqueta','gabardina','chaleco','parka','buzo','capa','cárdigan','saco','cazadora','saco','chubasquero','parka','manguitos','plumíferos','plumiferos','cardigan','rompevientos','jersey','sudadera'],['sobrecamisa','buzo','blazer']],
                [['sudadera','jogger','chándal'],['leggings', 'leggins','bicicletero', 'capri', 'cycling', 'ciclista'],['sport', 'sporty']],
                [['tenis','tennis','deportivas','deportivos'],['oxford','clásico','clasico','zuecos'],['sandalias','trespuntadas'],['baletas','spadrillas','bamba'],['tacones','tacón','zapatos','zapatillas'],['botas','botínes']],
                [['bolso','bandolera','cartera','mochila','riñonera','shopper','maletin','maletín','morral']],
                [['correa','gorro','bufanda','medias','cadenas','collares','aretes','anillos','tobilleras','broche']],[[]]],
    }
    categories = ["Camisas y Camisetas","Pantalones y Jeans","Vestidos y Enterizos","Faldas y Shorts","Abrigos y Blazers","Ropa deportiva","Zapatos","Bolsos","Accesorios","Otros"]
    cats = brands_categories[self.brand]
    cats2 = brands_subcategories[self.brand]
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
