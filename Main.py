import os, json, scrapy, requests, Bershka, Gef, MercedesCampuzano, PullAndBear, Stradivarius, Zara, Mango
from time import sleep
from random import uniform
from Item import Item, toInt
from Database import Database
from scrapy.crawler import CrawlerProcess

urlsDb = Database('Urls')
bDb = Database('Bershka')
# gDb = Database('Gef')
mngDb = Database('Mango')
mDb = Database('Mercedes Campuzano')
pDb = Database('Pull & Bear')
sDb = Database('Stradivarius')
zDb = Database('Zara')

def is_valid_json(path):
    try:
        with open(path, 'r', encoding='utf8') as f:
            j = json.loads(f.read())
        return True
    except:
        return False


def merge():
    totalItems = 0
    percentage = 0
    index = 0
    bar = ''
    path = './Database'
    files = []
    for file in os.listdir(path):
        files.append(file)
    for file in files:
        if '.json' in file and any(n in file for n in ['1','2','3','4','5','6']):
            with open('{}/{}'.format(path, file), 'r', encoding='utf8') as f:
                try:
                    j = json.loads(f.read())
                    totalItems+=len(j['Items'])
                    print(file,len(j['Items']))
                except:
                    pass
    for file in files:
        if '.json' in file and any(n in file for n in ['1','2','3','4','5','6']):
            print(file)
            with open('{}/{}'.format(path, file), 'r', encoding='utf8') as f:
                try:
                    j = json.loads(f.read())
                    for k in range(len(j['Items'])):
                        i=''
                        while not i:
                            try:
                                i = j['Items'][f'{k+1}']
                            except:
                                k+=1
                        if 'Bershka' == i['brand']:
                            db = bDb
                        elif 'Mercedes' in i['brand']:
                            db = mDb
                        elif 'Pull' in i['brand']:
                            db = pDb
                        elif 'Stradivarius' == i['brand']:
                            db = sDb
                        elif 'Zara' == i['brand']:
                            db = zDb
                        elif 'Mango' == i['brand']:
                            db = mngDb
                        db.add(Item(i['brand'],i['name'],i['description'],i['priceBefore'],i['allPricesNow'],i['discount'],i['allImages'],i['url'],i['allSizes'],i['colors'],i['category'],i['originalCategory'],i['subcategory'],i['originalSubcategory'],i['sale'],i['gender']))
                        index += 1
                        if not percentage == int(index / totalItems * 100):
                            percentage = int(index / totalItems * 100)
                            bar = '{}°'.format(bar)
                            print('{}% ({} de {}) {}'.format(percentage, index, totalItems, bar))
                except Exception as e:
                    print(e)
    # input('\nPresione enter para salir\n')


def scrap(brands = ['Mango','PullAndBear', 'Bershka', 'Stradivarius', 'MercedesCampuzano', 'Zara']):
    brands.reverse()
    for brand in brands:
        # s = time.localtime(time.time())
        # with open('Items/Log.txt', 'a', encoding='utf8') as f:
        #     f.write(f'Inicia {brand}: {s.tm_hour}:{s.tm_min}\n')
        try:
            exec('{0}.Scrap{0}()'.format(brand))
        except:
            print('Error scrapping', brand)
        # lastLoad = upload(lastLoad)
        # s = time.localtime(time.time())
        # with open('Items/Log.txt', 'a', encoding='utf8') as f:
        #     f.write(f'Acaba {brand}: {s.tm_hour}:{s.tm_min}\n\n')


def crawl(brands=['mercedescampuzano.com', 'zara.com']):

    class ItemsSpider(scrapy.Spider):
        name = 'Items'
        start_urls = urlsDb.get_crawl_urls(brands)
        headers = {'Connection': 'keep-alive','Cache-Control': 'max-age=0','DNT': '1','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36','Sec-Fetch-User': '?1','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'navigate','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'en-US,en;q=0.9',}
        def parse(self, response):
            def dataFromZaraJson(json):
                item = {}
                item['description'] = json['colors'][0]['description']
                output = []
                for color in json['colors']:
                    data = {'name': color['name'],'sizes' : [],'imgs' : []}
                    for s in color['sizes']:
                        a = '' if s['availability'] == 'in_stock' else '(Agotado)'
                        data['sizes'].append(f'{s["name"]}{a}')
                    for img in color['mainImgs']:
                        data['imgs'].append(
                            f'https://static.zara.net/photos//{img["path"]}/w/508/{img["name"]}.jpg?ts=1618487725904'
                        )
                    output.append(data)
                item['colors'] = output
                return item

            xpaths = {
                'Bershka': {
                    'category': '',
                    'color': './/ul[@class="swiper-wrapper"]/li/a/div/img/@scr',
                    'description': './/section[@class="product-info"]/text()',
                    'discount': './/span[@class="discount-tag"]/text()',
                    'imgs': './/div/button/div[@class="image-item-wrapper"]/img/@src',
                    'name': './/h1[@class="product-title"]/text()',
                    'priceBefore': './/span[@class="old-price-elem"]/text()',
                    'priceBefore2': './/span[@class="old-price-elem"]/text()',
                    'priceNow': './/div[contains(@class,"current-price-elem")]/text()',
                    'sizes': './/div[@class="sizes-list-detail"]/ul/li/button',
                    'stock': '',
                    'subCat': '',
                    'hasStock': '',
                },
                'Gef': {
                    'category': '',
                    'color': '',
                    'description': '',
                    'discount': '',
                    'imgs': '',
                    'name': '',
                    'priceBefore': '',
                    'priceBefore2': '',
                    'priceNow': '',
                    'sizes': '',
                    'stock': '',
                    'subCat': '',
                    'hasStock': '',
                },
                'Mercedes Campuzano': {
                    'category': './/a[@class="vtex-breadcrumb-1-x-link vtex-breadcrumb-1-x-link--1 dib pv1 link ph2 c-muted-2 hover-c-link"]/text()',
                    'color': './/img[@class="vtex-store-components-3-x-skuSelectorItemImageValue"]/@src',
                    'colorsBtn': './/ul[@class="vtex-slider-0-x-sliderFrame list pa0 h-100 ma0 flex justify-center"]/li[not(.//button)]',
                    'description': './/div[@class="vtex-store-components-3-x-content vtex-store-components-3-x-content--product-description h-auto"]//text()',
                    'description2': './/div[@class="vtex-store-components-3-x-specificationsTableContainer mt9 mt0-l pl8-l"]',
                    'discount': './/div[@class="vtex-store-components-3-x-discountInsideContainer t-mini white absolute right-0 pv2 ph3 bg-emphasis z-1"]//text()',
                    'hasStock': 'absolute absolute--fill vtex-store-components-3-x-diagonalCross',
                    'imgs': './/img[@class="vtex-store-components-3-x-productImageTag vtex-store-components-3-x-productImageTag--main"]/@src',
                    'name': './/span[@class="vtex-store-components-3-x-productBrand "]/text()',
                    'name2': './/span[contains(@class,"vtex-store-components-3-x-currencyInteger vtex-store-components-3-x-currencyInteger--price"]',
                    'priceBefore': './/div[@class="vtex-store-components-3-x-listPrice t-small-s t-small-ns c-muted-2 mb2 vtex-store-components-3-x-price_listPriceContainer vtex-store-components-3-x-price_listPriceContainer--price"]//text()',
                    'priceBefore2': './/div[@class="vtex-store-components-3-x-listPrice t-small-s t-small-ns c-muted-2 mb2 vtex-store-components-3-x-price_listPriceContainer vtex-store-components-3-x-price_listPriceContainer--price"]//text()',
                    'priceNow': './/div[@class="vtex-store-components-3-x-sellingPrice vtex-store-components-3-x-sellingPriceContainer pv1 b c-on-base vtex-store-components-3-x-price_sellingPriceContainer vtex-store-components-3-x-price_sellingPriceContainer--price"]//text()',
                    'sizes': './/div[@class="vtex-store-components-3-x-valueWrapper vtex-store-components-3-x-skuSelectorItemTextValue c-on-base center pl5 pr5 z-1 t-body"]/text()',
                    'stock': './/div[@class="vtex-store-components-3-x-skuSelectorInternalBox w-100 h-100 b--muted-4 br2 b z-1 c-muted-5 flex items-center overflow-hidden hover-b--muted-2 ba" and div[@class="vtex-store-components-3-x-valueWrapper vtex-store-components-3-x-skuSelectorItemTextValue c-on-base center pl5 pr5 z-1 t-body"]]/*[1]/@class',
                    'subCat': './/a[@class="vtex-breadcrumb-1-x-link vtex-breadcrumb-1-x-link--2 dib pv1 link ph2 c-muted-2 hover-c-link"]/text()',
                },
                'Pull & Bear': {
                    'category': '',
                    'color': '',
                    'description': '',
                    'discount': '',
                    'imgs': '',
                    'name': '',
                    'priceBefore': '',
                    'priceBefore2': '',
                    'priceNow': '',
                    'sizes': '',
                    'stock': '',
                    'subCat': '',
                    'hasStock': '',
                },
                'Zara': {
                    'category': './/div[@class="expandable-text__inner-content"]/p/text()',
                    'color': './/p[contains(@class,"product-detail-info__color")]',
                    'description': './/div[@class="expandable-text__inner-content"]/p/text()',
                    'discount': './/div[@class="product-detail-info__price-amount price"]/span/span/text()',
                    'imgs': './/div[@class="media__wrapper media__wrapper--fill media__wrapper--force-height"]/picture/img[@class="media-image__image media__wrapper--media"]/@src',
                    'name': './/h1[contains(@class,"info__name")]/text()',
                    'priceBefore': './/div[@class="product-detail-info__price-amount price"]/span[@class="price__amount price__amount--old"]/text()',
                    'priceNow': './/div[@class="product-detail-info__price-amount price"]/span[@class="price__amount" or @class="price__amount price__amount--on-sale"]/text()',
                    'sizes': './/span[contains(@class,"product-size-info__main-label")]/text()',
                    'stock': './/ul[contains(@id,"product-size-selector-product-detail-info-")]/li/@class',
                    'subCat': './/div[@class="expandable-text__inner-content"]/p/text()',
                    'hasStock': 'item--is-disabled',
                    'gender':'.//nav[@class="layout-footer-breadcrumbs"]/ol/li/a/span/text()'
                },
            }
            if 'bershka' in response.url:
                brand = 'Bershka'
                db = bDb
            #elif 'gef' in response.url:
            #    brand = 'Gef'
            #    db = gDb
            elif 'mercedes' in response.url:
                brand = 'Mercedes Campuzano'
                db = mDb
            elif 'zara' in response.url:
                brand = 'Zara'
                db = zDb
            elif all(w in response.url for w in ['pull', 'bear']):
                brand = 'Zara'
                db = pDb
            gender = 'Hombre' if 'hombre' in response.url else 'Mujer'
            sizes = []
            priceNow = toInt(response.xpath(xpaths[brand]['priceNow']).getall())
            priceBefore = toInt(response.xpath(xpaths[brand]['priceBefore']).getall())
            if priceBefore == 0:
                priceBefore = priceNow
            discount = ''.join(response.xpath(xpaths[brand]['discount']).getall()).replace(
                '\xa0', ''
            )
            name = response.xpath(xpaths[brand]['name']).get()
            description = response.xpath(xpaths[brand]['description']).get()
            imgs = []
            colors = []
            if brand == 'Zara':
                for split in response.xpath(xpaths[brand]['gender']).getall():
                    if 'MUJER' in split.upper():
                        gender = 'Mujer'
                    elif 'HOMBRE' in split.upper():
                        gender = 'Hombre'
                if gender == 'Mujer':
                    jsonData = response.xpath('.//body/script/text()').get()
                    jsonData = jsonData[jsonData.index('window.zara.viewPayload') + 26 : -1]
                    jsonData = json.loads(jsonData)
                    jsonData = jsonData['product']
                    category = jsonData['familyName']
                    if not name:
                        name = jsonData['name']
                    jsonData = jsonData['detail']
                    if priceNow == 0:
                        priceNow = int(jsonData['colors'][0]['price']/100)
                    if priceBefore == 0:
                        try:
                            priceBefore = int(jsonData['colors'][0]['oldPrice']/100)
                            discount = int(jsonData['colors'][0]['displayDiscountPercentage'])
                        except:
                            priceBefore = priceNow
                            discount = 0
                    jsonData = dataFromZaraJson(jsonData)
                    if not description:
                        description = jsonData['description']
                    for color in jsonData['colors']:
                        colors.append(color['name'])
                        imgs.append(color['imgs'])
                        sizes.append(color['sizes'])
            elif brand == 'Mercedes Campuzano':
                temp = [
                response.xpath(xpaths[brand]['sizes']).getall(),
                response.xpath(xpaths[brand]['stock']).getall()]
                for i in range(len(temp[0])):
                    if xpaths[brand]['hasStock'] in temp[1][i]:
                        sizes.append('{}(Agotado)'.format(temp[0][i]))
                    else:
                        sizes.append(temp[0][i])
                imgs = response.xpath(xpaths[brand]['imgs']).getall()
                if imgs:
                    if not (type(imgs[0])==list):
                        imgs = [imgs]
                colors = response.xpath(xpaths[brand]['color']).getall()
                temp.clear()
                category = response.xpath(xpaths[brand]['category']).get()
            if not priceBefore == 0:
                item = Item(
                    brand,
                    name,
                    description,
                    priceBefore,
                    priceNow,
                    discount,
                    imgs,
                    response.url,
                    sizes,
                    colors,
                    category,
                    category,
                    category,
                    category,
                    False,
                    gender,
                    crawling=True,
                )
                db.add(item)
            else:
                print('<<<<<<<<<<<<<<<<<<<<<<<<This item has no price:', response.url)
                urlsDb.urlError(response.url)
            sleep(uniform(5,10))
    process = CrawlerProcess(
        settings={
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
           }
    )
    process.crawl(ItemsSpider)
    process.start()

# Lambda AWS
def postItem(data):
    '''Create or update the element with the same url'''
    temp = jsonToBody(data)#.replace(''allPricesNow'',''allPriceNow'').replace(''allSizes'',''allSize'').replace(''subcategory'',''subCategory'').replace(''originalSubcategory'',''originalSubCategory'')
    try:
        return requests.post('https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/find', temp.encode('utf-8'))
    except Exception as e:
        print('Exception:',e)


def jsonToBody(json):
    for p in range(len(json['allPricesNow'])):
        json['allPricesNow'] = toInt(json['allPricesNow'][p])
    json['priceBefore'] = toInt(json['priceBefore'])    
    json['discount'] = toInt(json['discount'])
    json['id_producto'] = json['url']
    _backup=[
        json['allPricesNow'],
        json['allImages'],
        json['allSizes'],
        json['colors']
        ]
    json['allPricesNow'] = '__allPricesNow__'
    json['allImages'] = '__allImages__'
    json['allSizes'] = '__allSizes__'
    json['colors'] = '__colors__'
    return str(json).replace("'",'"').replace('"sale": True','"sale": 1').replace('"sale": False','"sale": 0').replace('"__allPricesNow__"',str(_backup[0])).replace('__allImages__',str(_backup[1])).replace('__allSizes__',str(_backup[2])).replace('__colors__',str(_backup[3])).replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U')


def post(databases = [mngDb, bDb, mDb, zDb, pDb, sDb]):
    totalItems = 0
    percentage = 0
    index = 0
    bar = ''
    for d in databases:
        totalItems += len(d.getAllItems())
    for d in databases:
        for i in d.getAllItems():
            postItem(i)
            index += 1
            if not percentage == int(index / totalItems * 100):
                percentage = int(index / totalItems * 100)
                bar = bar+'°'
                print(f'{percentage}% ({index} de {totalItems}) {bar}')


def check_sales(brands = ['PullAndBear', 'Bershka', 'Stradivarius', 'Zara', 'MercedesCampuzano']):
    for brand in brands:
        try:
            exec('{0}.ScrapSale()'.format(brand))
        except:
            print('Error scrapping Sale in', brand)

def update_local_list():
    '''Ensure that the databases exists. Copy original files and delete or just rename to `DB (copia)`'''
    databases = [Database('Bershka (copia)'), Database('Mercedes Campuzano (copia)'), Database('Pull & Bear (copia)'), Database('Stradivarius (copia)'),Database('Zara (copia)')]
    local = Database('Local')
    total_items = 0
    percentage = 0
    index = 0
    bar = ''
    for database in databases:
        for item in database.getAllItems():
            total_items+=1
    for database in databases:
        for item in database.getAllItems():
            local.addUrl(item['url'])
            index+=1
            if not percentage == int(index / total_items * 100):
                percentage = int(index / total_items * 100)
                bar = f'{bar}°'
                print(f'{percentage}% ({index} de {total_items}) {bar}')

def delete_brands_fron_urlsdb(brands):
    to_delete = []
    for item in urlsDb.getAllUrls():
        if any(b in item['url'] for b in brands):
            to_delete.append(item['url'])
    for url in to_delete:
        urlsDb.delete(url)
    print(to_delete)
    response = requests.post('https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/delete', f'{{"data": {to_delete}}}'.replace(''','''))
    print(response.json())
    return response

def delete():
    '''Delete the specified list from remote database'''
    to_delete = []
    for item in urlsDb.getAllUrls():
        if 'bershka' in item['url']:
            if not bDb.contains(item['url']):
                to_delete.append(item['url'])
        elif 'mercedescampuzano' in item['url']:
            if not mDb.contains(item['url']):
                to_delete.append(item['url'])
        elif 'pullandbear' in item['url']:
            if not pDb.contains(item['url']):
                to_delete.append(item['url'])
        elif 'stradivarius' in item['url']:
            if not sDb.contains(item['url']):
                to_delete.append(item['url'])
        elif 'zara' in item['url']:
            if not zDb.contains(item['url']):
                to_delete.append(item['url'])
    for url in to_delete:
        urlsDb.delete(url)
    print(to_delete,len(to_delete))
    return requests.post('https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/delete', f'{{"data": {to_delete}}}'.replace("'",'"')).json()
    
# Main code
# update_local_list()
# merge()
# delete_brands_fron_urlsdb(['stradivarius'])

scrap()
# different_categores=['BLASIER: Abrigos y Blazers - Blazers','BLASIER: Abrigos y Blazers - Abrigos y Blazers','CHALECO: Abrigos y Blazers - Abrigos','CHAQUETA: Abrigos y Blazers - Blazers','BLASIER: Abrigos y Blazers - Abrigos','VESTIDO: Vestidos y Enterizos - Vestidos','VESTIDO: Camisas y Camisetas - Camisas y Camisetas','VESTIDO: Abrigos y Blazers - Blazers','MONO: Vestidos y Enterizos - Vestidos','FALDA: Faldas y Shorts - Faldas','VESTIDO: Otros - Otros','VESTIDO: Abrigos y Blazers - Abrigos','VESTIDO: Ropa deportiva - Sudaderas','CAMISA: Camisas y Camisetas - Camisas','VESTIDO: Camisas y Camisetas - Camisetas','ABRIGO: Vestidos y Enterizos - Enterizos','PETO: Otros - Otros','PANTALON: Pantalones y Jeans - Jeans', 'VESTIDO: Vestidos y Enterizos - Vestidos','TOPS Y OTRAS P.: Camisas y Camisetas - Camisas y Camisetas','VESTIDO: Abrigos y Blazers - Abrigos','CAMISA: Camisas y Camisetas - Camisas','CHALECO: Abrigos y Blazers - Abrigos','VESTIDO: Otros - Otros','TOPS Y OTRAS P.: Camisas y Camisetas - Tops','CAMISA: Vestidos y Enterizos - Vestidos y Enterizos','CAMISA: Camisas y Camisetas - Tops','CAMISA: Camisas y Camisetas - Camisetas','BODY: Otros - Otros','CAMISA: Otros - Otros','CAMISETA: Otros - Otros','JERSEY: Camisas y Camisetas - Tops','TOPS Y OTRAS P.: Camisas y Camisetas - Camisetas','CAMISETA: Camisas y Camisetas - Tops','JERSEY: Camisas y Camisetas - Camisetas','TOPS Y OTRAS P.: Camisas y Camisetas - Camisas','CAMISA: Vestidos y Enterizos - Enterizos','CHAQUETA: Abrigos y Blazers - Abrigos','CHALECO: Vestidos y Enterizos - Vestidos y Enterizos','CAZADORA: Otros - Otros','CAMISETA: Vestidos y Enterizos - Vestidos y Enterizos','MONO: Camisas y Camisetas - Camisetas','CAMISETA: Camisas y Camisetas - Camisetas']
# crawl(['mercedescampuzano.com'])
post()
# print(delete())


# TESTING
# d={'brand': 'brand', 'name': 'Camiseta básica manga corta', 'description': ' ', 'priceBefore': 79900, 'allPricesNow': [35900], 'discount': 0, 'allImages': [['https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/511/2500151511_1_1_2.jpg?t=1619013088469', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/511/2500151511_2_1_2.jpg?t=1619013088469', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/511/2500151511_2_2_2.jpg?t=1619013088469', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/511/2500151511_2_3_2.jpg?t=1619013088469', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/511/2500151511_2_4_2.jpg?t=1618568296170'], ['https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/602/2500151602_1_1_2.jpg?t=1607945209004', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/602/2500151602_2_1_2.jpg?t=1607945209004', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/602/2500151602_2_2_2.jpg?t=1607945209004', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/602/2500151602_2_3_2.jpg?t=1607945209004', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/602/2500151602_2_4_2.jpg?t=1607945209004'], ['https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/010/2500151010_1_1_2.jpg?t=1610018595147', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/010/2500151010_2_1_2.jpg?t=1610018595147', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/010/2500151010_2_2_2.jpg?t=1610018595147', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/010/2500151010_2_3_2.jpg?t=1610018595147', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/010/2500151010_2_4_2.jpg?t=1609244762972', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/010/2500151010_6_1_2.jpg?t=1609244762972'], ['https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/001/2500151001_1_1_2.jpg?t=1618910149836', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/001/2500151001_2_1_2.jpg?t=1618910149836', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/001/2500151001_2_2_2.jpg?t=1618910149836', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/001/2500151001_2_3_2.jpg?t=1618910149836', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/001/2500151001_2_4_2.jpg?t=1603719197259', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/001/2500151001_6_1_2.jpg?t=1603719197259'], ['https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/003/2500151003_1_1_2.jpg?t=1615993284890', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/003/2500151003_2_1_2.jpg?t=1615993284890', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/003/2500151003_2_2_2.jpg?t=1615993284890', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/003/2500151003_2_3_2.jpg?t=1615993284890', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/003/2500151003_2_4_2.jpg?t=1612959901701', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/003/2500151003_6_1_2.jpg?t=1612959901701']], 'url': 'https://www.stradivarius.com/co/new-collection/ropa/compra-por-producto/camisetas/ver-todo/camiseta-b%C3%A1sica-manga-corta-c1020047036p302047651.html', 'allSizes': [['XS(Agotado)', 'S(Agotado)', 'M(Agotado)', 'L', 'XL'], ['XS', 'S', 'M', 'L', 'XL'], ['XS', 'S', 'M', 'L', 'XL'], ['XS', 'S', 'M', 'L', 'XL'], ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']], 'colors': ['https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/511/2500151511_3_1_5.jpg?t=1619013088469', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/602/2500151602_3_1_5.jpg?t=1607945209004', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/010/2500151010_3_1_5.jpg?t=1610018595147', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/001/2500151001_3_1_5.jpg?t=1618910149836', 'https://static.e-stradivarius.net/5/photos3/2021/V/0/1/p/2500/151/003/2500151003_3_1_5.jpg?t=1615993284890'], 'category': 'Camisas y Camisetas', 'originalCategory': 'Camisetas', 'subcategory': 'Camisetas', 'originalSubcategory': 'Camisetas', 'sale': True, 'gender': 'Mujer'}
# sDb.add(it)
#it = Item(d['brand'],d['name'],d['description'],d['priceBefore'],d['allPricesNow'],d['discount'],d['allImages'],d['url'],d['allSizes'],d['colors'],d['category'],d['originalCategory'],d['subcategory'],d['originalSubcategory'],d['sale'],d['gender'])
