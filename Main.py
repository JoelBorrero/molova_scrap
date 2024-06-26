#TODO ocultar si no hay disponibilidad, enviar categorias no linkeadas

import os
import ast
import json
# import scrapy
import requests
from time import sleep
# from random import uniform

from selenium import webdriver
# from scrapy.crawler import CrawlerProcess
import Bershka, Mango, MercedesCampuzano, PullAndBear, Stradivarius, Zara

from Item import Item, toInt
from Database import Database
from Widgets import LoadingBar


bDb = Database('Bershka')
mDb = Database('Mercedes Campuzano')
mngDb = Database('Mango')
pDb = Database('Pull & Bear')
sDb = Database('Stradivarius')
zDb = Database('Zara')
broken = Database('Broken')
latest = Database('Latest')

def merge(databases = [bDb, mDb, zDb, pDb, sDb, mngDb]):
    path = './Database'
    total_urls = 0
    for db in databases:
        total_urls += len(db.getAllUrls())
    for file in os.listdir(path):
        if '.json' in file and any(n in file for n in ['1','2','3','4','5','6']):
            print(file)
            with open('{}/{}'.format(path, file), 'r', encoding='utf8') as f:
                try:
                    j = json.loads(f.read())
                    bar = LoadingBar(len(j['Items']))
                    for _, index in j['Items']:
                        i = j['Items'][index]
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
                        try:
                            ref = i['ref']
                        except:
                            ref = ''
                        db.add(Item(i['brand'], i['name'],ref,i['description'], i['priceBefore'], i['allPricesNow'], i['discount'], i['allImages'], i['url'], i['allSizes'], i['colors'], i['category'], i['originalCategory'], i['subcategory'], i['originalSubcategory'], i['sale'], i['gender']), sync=True)
                        bar.update()
                except Exception as e:
                    print(e)
    total_urls = []
    for db in databases:
        total_urls.extend(db.getAllUrls())
    with open('./URLS_NEW.txt','w') as f:
        f.write(str(total_urls))
    # input('\nPresione enter para salir\n')

def scrap(brands = ['PullAndBear', 'Bershka', 'MercedesCampuzano']):
    for brand in brands:
        print('>>>>> ',brand,' <<<<<')
        try:
            exec('{0}.Scrap{0}()'.format(brand))
        except Exception as e:
           print('Error scrapping', brand, e)

"""
    def crawl(brands=['mercedescampuzano.com', 'zara.com']):
    class ItemsSpider(scrapy.Spider):
        name = 'Items'
        start_urls = [] #urlsDb.get_crawl_urls(brands)
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
            sleep(uniform(5,10))
    process = CrawlerProcess(
        settings={
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
           }
    )
    process.crawl(ItemsSpider)
    process.start()"""

def postItem(data):
    '''Create or update the element with the same url'''
    temp = jsonToBody(data)#.replace(''allPricesNow'',''allPriceNow'').replace(''allSizes'',''allSize'').replace(''subcategory'',''subCategory'').replace(''originalSubcategory'',''originalSubCategory'')
    try:
        return requests.post('https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/find', temp.encode('utf-8'))
    except Exception as e:
        print('Exception:',e)

def jsonToBody(json):
    try:
        for p in range(len(json['allPricesNow'])):
            json['allPricesNow'] = toInt(json['allPricesNow'][p])
    except:
        json['allPricesNow'] = toInt(json['allPricesNow'])
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

def post(databases = [bDb, mDb, pDb, zDb, mngDb, sDb], crawling=False):
    if crawling:
        databases = databases[3:]
    else:
        databases = databases[:3]
    total_items = 0
    for d in databases:
        total_items += len(d.getAllUrls())
    bar = LoadingBar(total_items)
    for d in databases:
        for i in d.getAllItems():
            postItem(i)
            bar.update()

def check_broken_links(databases = [bDb, mDb, zDb, pDb, sDb], start=0, crawling=False):
    '''Check each url that was not present in the last scrap'''
    print('Looking for broken links...')
    to_delete = []
    for db in databases:
        urls = []
        for url in db.getAllUrls():
            if not latest.contains_url(url):
                urls.append(url)
        if len(db.getAllUrls()) - len(urls) > 200:
            to_delete.extend(urls)
    print(len(to_delete),'items to review')
    if not crawling and to_delete:
        driver = webdriver.Chrome('./chromedriver')
        driver.maximize_window()
        driver.set_page_load_timeout(30)
        for url in to_delete[start:]:
            if not start%10:
                print(start)
            start+=1
            try:
                driver.get(url)
            except:
                driver.quit()
                sleep(5)
                driver = webdriver.Chrome('./chromedriver')
                driver.maximize_window()
                driver.set_page_load_timeout(20)
                driver.get(url)
            try:
                brand = Bershka if 'bershka.com' in url else Mango if 'mango.com' in url else MercedesCampuzano if 'mercedescampuzano.com' in url else PullAndBear if 'pullandbear.com' in url  else Stradivarius if  'stradivarius.com' in url else Zara
                if not driver.find_elements_by_xpath(brand.xpaths['name']):
                    sleep(2)
                if not driver.find_elements_by_xpath(brand.xpaths['name']):
                    if not driver.find_elements_by_xpath(brand.xpaths['imgs']):
                        broken.db.insert({'url':url})
                        brand.db.delete(url)
                else:
                    try:
                        try:
                            priceBfr = driver.find_element_by_xpath(brand.xpaths['priceBfr']).text
                        except:
                            sleep(1)
                            priceBfr = driver.find_element_by_xpath(brand.xpaths['priceBfr']).text
                        try:
                            priceNow = driver.find_element_by_xpath(brand.xpaths['priceNow']).text
                            discount = 0 # driver.find_element_by_xpath(brand.xpaths['discount']).text
                        except:
                            priceNow = priceBfr
                            discount = 0
                        brand.db.update_product([discount, priceBfr, priceNow], url)
                    except Exception as e:
                        print('Error updating:',url,e)
            except:
                print('Error getting')
        to_delete.extend(broken.getAllUrls())
        driver.quit()
    if to_delete:
        print(len(to_delete),'items deleted')
        open('./Database/Latest.json', 'w').close()
        open('./Database/Broken.json', 'w').close()
        requests.post('https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/delete', f'{{"data": {to_delete}}}'.replace("'",'"')).json()

def sync(brand=''):
    if brand in ['Bershka', 'Mango', 'Mercedes Campuzano', 'Pull & Bear', 'Stradivarius', 'Zara']:
        brand = f'marcas/{brand}'
    else:
        brand = 'coleccion'
        for db in [bDb, mDb, mngDb, pDb, sDb, zDb, broken, latest]:
            db.clear()
    for last in ['Camisas y Camisetas','Pantalones y Jeans','Vestidos y Enterizos','Faldas y Shorts','Abrigos y Blazers','Ropa Deportiva', 'Zapatos','Bolsos','Accesorios']:
        for index in [0,1]:
            endpoint = f'https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/{brand}/{index}/{last}'.replace(' ','%20')
            print(last,'sale' if index else 'col')
            res = requests.get(endpoint).json()
            if 'items' in res:
                bar = LoadingBar(len(res['items']))
                i = 0
                for item in res['items']:
                    db = get_database(item['brand'])
                    for pop in ['data', 'date_time', 'id', 'id_producto']:
                        item.pop(pop)
                    if not type(item['allPricesNow']) == list:
                        item['allPricesNow'] = [item['allPricesNow']]
                    db.add(item, sync=True)
                    index += 1
                    i += 1
                    bar.update()
            else:
                print('ERROR:'+endpoint)

def clear_remote_db():
    driver = webdriver.Chrome("./chromedriver")
    driver.maximize_window()
    driver.set_page_load_timeout(10)
    for last in ['Camisas y Camisetas','Pantalones y Jeans','Vestidos y Enterizos','Faldas y Shorts','Abrigos y Blazers','Ropa Deportiva', 'Zapatos','Bolsos','Accesorios']:
        for index in [0,1]:
            to_delete = []
            endpoint = f"https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/coleccion/{index}/{last}".replace(' ','%20')
            res = requests.get(endpoint).json()
            for item in res['items']:
                url = item['id_producto']
                driver.get(url)
                brand = Bershka if 'bershka.com' in url else Mango if 'mango.com' in url else MercedesCampuzano if 'mercedescampuzano.com' in url else PullAndBear if 'pullandbear.com' in url  else Stradivarius if  'stradivarius.com' in url else Zara
                if not driver.find_elements_by_xpath(brand.xpaths['name']):
                    sleep(1)
                if not driver.find_elements_by_xpath(brand.xpaths['name']):
                    if not driver.find_elements_by_xpath(brand.xpaths['imgs']):
                        broken.db.insert({'url':url})
                        print(url,'borrado')
                        brand.db.delete(url)
                        to_delete.append(url)
            requests.post('https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/delete', f'{{"data": {to_delete}}}'.replace("'",'"')).json()

def scrap_for_links():
    for brand in [Mango, Stradivarius, Zara]:
        brand.scrap_for_links()

def get_database(brand):
    brand = brand.lower()
    if 'bershka' in brand:
        return bDb
    elif 'mercedes' in brand:
        return mDb
    elif all(pb in brand for pb in ['pull', 'bear']):
        return pDb
    elif 'stradivarius' in brand:
        return sDb
    elif 'zara' in brand:
        return zDb
    elif 'mango' in brand:
        return mngDb

def remove_brand(brand):
    if brand and brand in ['Bershka', 'Mango', 'Mercedes Campuzano', 'Pull & Bear', 'Stradivarius', 'Zara']:
        brand = f'marcas/{brand}'
        for last in ['Camisas y Camisetas','Pantalones y Jeans','Vestidos y Enterizos','Faldas y Shorts','Abrigos y Blazers','Ropa Deportiva', 'Zapatos','Bolsos','Accesorios']:
            for index in [0,1]:
                endpoint = f'https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/{brand}/{index}/{last}'.replace(' ','%20')
                res = requests.get(endpoint).json()
                to_delete = [item['id_producto'] for item in res['items']]
                requests.post('https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/delete', f'{{"data": {to_delete}}}'.replace("'",'"')).json()
                print(last, len(to_delete))

    else:
        print('Marca no encontrada')

# Main code
def main():
    print('Comma separated(1,2,3)\n1. Merge\n2. Scrap\n3. Check for broken links\n4. Post\n5. Sync\n6. Clear remote db')
    to_do = input('>')
    tasks = ['merge()','scrap()', 'check_broken_links()', 'post()', 'sync()','clear_remote_db()']
    for task in to_do.split(','):
        try:
            exec(tasks[int(task)-1])
        except Exception as e:
            print(e)
