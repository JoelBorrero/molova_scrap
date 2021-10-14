#TODO ocultar si no hay disponibilidad, enviar categorias no linkeadas
#  TODO " endpoints: crear y eliminar"

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
from JoelDB import JoelDB

from Item import Item, toInt
from Database import Database
from Widgets import LoadingBar


bDb = Database('Bershka')
mDb = Database('Mercedes Campuzano')
mngDb = Database('Mango')
pDb = Database('Pull & Bear')
sDb = Database('Stradivarius')
zDb = Database('Zara')
broken = JoelDB('Broken')
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
                        db.add(Item(i['brand'], i['name'],ref,i['description'], i['priceBefore'], i['allPricesNow'], i['discount'], i['allImages'], i['url'], i['allSizes'], i['colors'], i['category'], i['originalCategory'], i['subcategory'], i['originalSubcategory'], i['gender']), sync=True)
                        bar.update()
                except Exception as e:
                    print(e)
    total_urls = []
    for db in databases:
        total_urls.extend(db.getAllUrls())
    with open('./URLS_NEW.txt','w') as f:
        f.write(str(total_urls))
    # input('\nPresione enter para salir\n')


def scrap(brands = ['MercedesCampuzano']):
    for brand in brands:
        print('>>>>> ',brand,' <<<<<')
        try:
            exec('{0}.Scrap{0}()'.format(brand))
        except Exception as e:
           print('Error scrapping', brand, e)


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
    _backup=[json['allPricesNow'], json['allImages'], json['allSizes'], json['colors']]
    json['allPricesNow'] = '__allPricesNow__'
    json['allImages'] = '__allImages__'
    json['allSizes'] = '__allSizes__'
    json['colors'] = '__colors__'
    return str(json).replace("'",'"').replace('"sale": True','"sale": 1').replace('"sale": False','"sale": 0').replace('"__allPricesNow__"',str(_backup[0])).replace('__allImages__',str(_backup[1])).replace('__allSizes__',str(_backup[2])).replace('__colors__',str(_backup[3])).replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U')


def post(databases = [mDb, pDb, bDb, zDb, mngDb, sDb]):
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
                if not driver.find_elements_by_xpath(brand.XPATHS['name']):
                    sleep(2)
                if not driver.find_elements_by_xpath(brand.XPATHS['name']):
                    if not driver.find_elements_by_xpath(brand.XPATHS['imgs']):
                        broken.db.insert({'url':url})
                        brand.db.delete(url)
                else:
                    try:
                        try:
                            priceBfr = driver.find_element_by_xpath(brand.XPATHS['priceBfr']).text
                        except:
                            sleep(1)
                            priceBfr = driver.find_element_by_xpath(brand.XPATHS['priceBfr']).text
                        try:
                            priceNow = driver.find_element_by_xpath(brand.XPATHS['priceNow']).text
                            discount = 0 # driver.find_element_by_xpath(brand.XPATHS['discount']).text
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
        latest.clear()
        broken.clear()
        delete(to_delete)


def sync(brand=''):
    if brand in ['Bershka', 'Mango', 'Mercedes Campuzano', 'Pull & Bear', 'Stradivarius', 'Zara']:
        brand = f'marcas/{brand}'
        db = get_database(brand)
        db.clear()
    else:
        brand = 'coleccion'
        for db in [bDb, mDb, mngDb, pDb, sDb, zDb, broken, latest]:
            db.clear()
    for last in ['Camisas y Camisetas', 'Pantalones y Jeans', 'Vestidos y Enterizos', 'Faldas y Shorts', 'Abrigos y Blazers', 'Ropa Deportiva', 'Zapatos', 'Bolsos', 'Accesorios']:
        for index in [0,1]:
            endpoint = f'https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/{brand}/{index}/{last}'.replace(' ','%20')
            print(last,'sale' if index else 'col')
            res = requests.get(endpoint).json()
            if 'items' in res:
                bar = LoadingBar(len(res['items']))
                for item in res['items']:
                    db = get_database(item['brand'])
                    # for pop in ['data', 'date_time', 'id', 'id_producto']:
                    #     item.pop(pop)
                    # if not type(item['allPricesNow']) == list:
                    #     item['allPricesNow'] = [item['allPricesNow']]
                    item = Item(item['brand'], item['name'],'ref',item['description'], item['priceBefore'], item['allPricesNow'], item['discount'], item['allImages'], item['url'], item['allSizes'], item['colors'], item['category'], item['originalCategory'], item['subcategory'], item['originalSubcategory'], item['gender'])
                    db.add(item, sync=True)
                    index += 1
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
                if not driver.find_elements_by_xpath(brand.XPATHS['name']):
                    sleep(1)
                if not driver.find_elements_by_xpath(brand.XPATHS['name']):
                    if not driver.find_elements_by_xpath(brand.XPATHS['imgs']):
                        broken.db.insert({'url':url})
                        print(url,'borrado')
                        brand.db.delete(url)
                        to_delete.append(url)
            delete(to_delete)


def scrap_for_links():
    for brand in [Bershka, Mango, Stradivarius, Zara]:
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
                delete(to_delete)
                print(last, len(to_delete))

    else:
        print('Marca no encontrada')


def delete(to_delete):
    return requests.post('https://2ksanrpxtd.execute-api.us-east-1.amazonaws.com/dev/molova/delete', f'{{"data": {to_delete}}}'.replace("'",'"')).json()


def main():
    print('Comma separated(1,2,3)\n1. Merge\n2. Scrap\n3. Check for broken links\n4. Post\n5. Sync\n6. Clear remote db')
    to_do = input('>')
    tasks = ['merge()','scrap()', 'check_broken_links()', 'post()', 'sync()','clear_remote_db()']
    for task in to_do.split(','):
        try:
            exec(tasks[int(task)-1])
        except Exception as e:
            print(e)
