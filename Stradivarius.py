import os
import ast
import requests
from time import sleep
from random import uniform
from datetime import datetime
import pytz

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Item import Item
from Database import Database

brand = 'Stradivarius'
db = Database(brand)
# db = Database(brand+'API')
tz = pytz.timezone('America/Bogota')
xpaths={
    'categories':'.//div[@class="categories-menu "]/div[contains(@class,"items-menu")]/div/a[not(@href="javascript:void(0)")]|.//div[@class="categories-menu "]/div[contains(@class,"items-menu")]/div[./a[@href="javascript:void(0)"]]/following-sibling::div[position()=1]//a',
    'categoriesSale':'.//ul[@class="product-categories"]/li/ul/li/a[span[contains(@style,"#f")]]',
    'colorsBtn':'.//div[@class="set-colors-product parent-center-child"]//img[@src]',
    'description':'.//span[@class="c-product-info--description-text"]',
    'discount':'.//div[@class="discount-percentage"]',
    'elems':'.//div[@class="product-grid-item item-generic-grid item-one-position-grid-2"]',
    'fast_priceBfr':'./div[@class="item-data-product"]/div/div/div/div/div[@class="one-old-price"]/div/span',
    'fast_priceNow':'./div[@class="item-data-product"]/div/div/div/div/div[@class="current-price"]/div/span',
    'fast_discount':'./div[@class="item-data-product"]/div/div/div/div/div[@class="discount-percentage"]',
    'href':'./div/a[@id="hrefRedirectProduct"]',
    'imgs':'.//div[@class="image-container"]/img',
    'main_categories':'.//div[contains(@class,"menu-list-item main-category ")]',
    'name':'.//h1[@class="product-name-title"]',
    'priceBfr':'.//div[@class="product-price block-height"]//div[@class="one-old-price"]//span',
    'priceNow':'.//div[@class="product-price block-height"]//div[@class="current-price"]//span',
    'priceNow2':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div/span',
    'ref': './/div[@class="product-ref-details block-height "]/span',
    'sizesTags':'.//div[@id="productComponentRight"]//div[@class="size-grid-sizes-container"]//span',
    'subCats':'.//div[@class="display-inline-block child-center-parent slider-items-container"]/div/a',
    'subCats2':'.//div[@class="category-badges-list"]/a[not(text()="Ver todo")]'}

endpoints = [('https://www.stradivarius.com/co/mujer/home-%26-living/compra-por-producto/papeler%C3%ADa-c1020367598.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367598/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/home-%26-living/compra-por-producto/decoraci%C3%B3n-c1020367623.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367623/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/pijamas/calzado-c1020367661.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367659/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/pijamas/lencer%C3%ADa-c1020367660.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367659/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/pijamas/pijamas-c1020367658.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367659/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/pijamas/ver-todo-c1020367659.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367659/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/pijamas-c1020367657.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367659/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/accesorios/compra-por-producto/gafas-c1393014.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1393014/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/accesorios/compra-por-producto/accesorios-de-pelo-c1393013.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1393013/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/accesorios/compra-por-producto/correas-c1393011.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1393011/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/accesorios/compra-por-producto/bisuter%C3%ADa/ver-todo-c1718569.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1718569/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/accesorios/compra-por-producto/monederos-c1695503.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1695503/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/zapatos/compra-por-producto/baletas-c1399024.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1399024/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/zapatos/compra-por-producto/sandalias-c1020001528.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020001528/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/zapatos/compra-por-producto/tenis-c1399023.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1399023/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/zapatos/compra-por-producto/todos/todos-c1020178528.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020178528/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/str-teen/calzado-c1020367571.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367566/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/str-teen/vestidos-c1020367568.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367566/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/str-teen/punto-c1020367565.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367566/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/str-teen/camisetas-c1020367564.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367566/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/str-teen/pantalones-c1020367563.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367566/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/str-teen/jeans-c1020367572.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367566/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/str-teen/shorts-c1020367570.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367566/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/str-teen/ver-todo-c1020367566.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367566/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/sport/compra-por-producto/partes-de-abajo/ver-todo-c1020367546.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367546/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/sport/compra-por-producto/partes-de-arriba-c1020367551.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367551/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/sport/compra-por-producto/conjuntos-combinados-c1020385315.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020385315/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/sport/compra-por-producto/ver-todo/ver-todo-c1020367540.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020367540/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/packs-c1020371005.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020371005/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/shorts/ver-todo-c1020377546.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020377546/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/faldas/ver-todo-c1718525.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1718525/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/camisas/ver-todo-c1718502.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1718502/product?languageId=-48&appId=1'), ('https://www.stradivarius.com/co/mujer/nuevo-c1020093507.html', 'https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020093507/product?languageId=-48&appId=1')]

class ScrapStradivarius:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.set_page_load_timeout(30)
        self.driver.maximize_window()
        self.driver.get('https://www.stradivarius.com/co/')
        try:
            sleep(3)
            self.driver.find_element_by_xpath('.//button[@class="STRButton  cancel-button STRButton_secondary STRButton_large"]').click()
        except:
            print('No dismiss cookies')
        # try:
        #     self.driver.find_element_by_xpath('.//div[@class="burger-icon"]').click()
        #     sleep(2)
        # except:
        #     print('No menu open')
        # main_categories = self.driver.find_elements_by_xpath(xpaths['main_categories'])
        main_categories = self.driver.find_elements_by_xpath(xpaths['categories'])
        categories = [[],[]]
        # for i in range(len(main_categories)):
        #     i=main_categories[i]
        #     self.driver.execute_script('arguments[0].scrollIntoView();', i)
        #     if i.find_elements_by_xpath('./a[contains(@href,"javascript")]'):
        #         try:
        #             i.click()
        #             sleep(3)
        #             for c in self.driver.find_elements_by_xpath(xpaths['categories']):
        #                 if not c.get_attribute('href') in categories[1]:
        #                     categories[0].append(c.get_attribute('innerText'))
        #                     categories[1].append(c.get_attribute('href'))
        #         except:
        #             print('err')
        #     else:
        #         categories[0].append(i.text)
        #         categories[1].append(i.find_element_by_xpath('./a').get_attribute('href'))
        #     main_categories = self.driver.find_elements_by_xpath(xpaths['main_categories'])
        for c in main_categories:
            if not 'javascript:void' in c.get_attribute('href'):
                categories[0].append(c.get_attribute('innerText'))
                categories[1].append(c.get_attribute('href'))
        for c in range(len(categories[0])):
            self.category = categories[0][c]
            self.originalCategory = categories[0][c]
            self.subcategory = categories[0][c]
            self.originalSubcategory = categories[0][c]
            self.sale = False
            self.scrapCategory(categories[1][c])
        self.driver.quit()
        # APICrawler()


    def scrapCategory(self, url):
        self.driver.get(url)
        sleep(1)
        subCats = [self.driver.find_elements_by_xpath(xpaths['subCats']),[]]
        if not subCats:
            sleep(1)
            subCats = [self.driver.find_elements_by_xpath(xpaths['subCats']),[]]
        if not subCats:
            sleep(5)
            subCats = [self.driver.find_elements_by_xpath(xpaths['subCats']),[]]
        for i in range(len(subCats[0])):
            subCats[1].append(subCats[0][i].find_element_by_xpath('./div[@class="name"]').text)
            subCats[0][i]=subCats[0][i].get_attribute('href')
        if subCats[0]:
            for i in range(len(subCats[0])):
                self.subcategory = subCats[1][i]
                self.originalSubcategory = subCats[1][i]
                self.scrapSubcategory(subCats[0][i])
        else:
            self.scrapSubcategory(url)

    def scrapSubcategory(self, url):
        self.driver.get(url)
        sleep(5)
        loading = True
        elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        while loading:
            try:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(3)
                self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_UP)
                sleep(1)
                self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_UP)
                sleep(2)
                loading = len(elems) < len(self.driver.find_elements_by_xpath(xpaths['elems']))
                elems = self.driver.find_elements_by_xpath(xpaths['elems'])
            except:
                loading = False
        for elem in elems:
            try:
                self.driver.execute_script('arguments[0].scrollIntoView();', elem)
                href = elem.find_element_by_xpath(xpaths['href']).get_attribute('href')
                try:
                    img = elem.find_element_by_xpath('.//img').get_attribute('src')
                except:
                    img = ''
                if db.contains(href, img):
                    db.update_product(elem, href, xpaths)
                else:
                    self.scrapProduct(href)
            except:
                print('Error')
            

    def scrapProduct(self, url):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            sleep(3)
            name = self.driver.find_elements_by_xpath(xpaths['name'])
            if not name:
                sleep(3)
                name = self.driver.find_elements_by_xpath(xpaths['name'])
            ref = self.driver.find_element_by_xpath(xpaths['ref']).text
            try:
                description = self.driver.find_element_by_xpath(xpaths['description']).text.capitalize()
            except:
                description = ' '
            priceNow = self.driver.find_element_by_xpath(xpaths['priceNow']).text
            try:
                priceBfr = self.driver.find_element_by_xpath(xpaths['priceBfr']).text
            except:
                priceBfr = priceNow
            try:
                discount = self.driver.find_element_by_xpath(xpaths['discount']).text
            except:
                discount = ' '
            colorsBtn = self.driver.find_elements_by_xpath(xpaths['colorsBtn'])
            colors = []
            allSizes = []
            allImages = []
            for c in colorsBtn:
                c.click()
                colors.append(c.get_attribute("src"))
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath(xpaths['sizesTags'])
                for s in sizesTags:
                    sizes.append(s.text)
                if len(sizesTags) == 0:
                    sizes = ["Única"]
                allSizes.append(sizes)
                images = []
                for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                    images.append(i.get_attribute("src"))
                allImages.append(images)
            if not allImages:
                images = []
                for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                    images.append(i.get_attribute("src"))
                allImages.append(images)
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath(xpaths['sizesTags'])
                for s in sizesTags:
                    sizes.append(s.text)
                if len(sizesTags) == 0:
                    allSizes.append(["Única"])
            if name and allImages:
                name = name[0].text.capitalize()
                if not self.originalSubcategory:
                    self.originalSubcategory = ' '
                item = Item(brand,name,ref,description,priceBfr,priceNow,discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale,"Mujer")
                db.add(item)
            else:
                print("Hubo un error")
        except Exception as e:
            print("Item saltado", url)
            print(e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


def scrap_for_links():
    driver = webdriver.Chrome('./chromedriver')
    driver.set_page_load_timeout(30)
    driver.maximize_window()
    driver.get('https://www.stradivarius.com/co/')
    try:
        sleep(3)
        driver.find_element_by_xpath('.//button[@class="STRButton  cancel-button STRButton_secondary STRButton_large"]').click()
    except:
        print('No dismiss cookies')
    main_categories = []
    for c in driver.find_elements_by_xpath(xpaths['categories']):
        main_categories.append(c.get_attribute('href'))
    get_network = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;'
    endpoints.clear()
    for c in main_categories:
        if not 'javascript:void' in c:
            driver.get(c)
            sleep(1)
            netData = driver.execute_script(get_network)
            for i in netData:
                if all(e in i['name'] for e in ['https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/','product?']) and i['name'] not in endpoints:
                    endpoints.insert(0,(c,i['name']))
    driver.quit()
    settings = ast.literal_eval(open('./Settings.txt','r').read())
    settings[brand]['endpoints']=endpoints
    with open('./Settings.txt','w') as s:
        s.write(str(settings))


class APICrawler:
    def __init__(self, endpoints):
        session = requests.session()
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'es-US,es;q=0.9',
            'content-type': 'application/json',
            'cookie': 'ITXSESSIONID=182592649f55aa1d98689723945fba3c; _abck=98D0A42A991781EA9192E81AB1B3DA3F~-1~YAAQT/1Vvs+4hLh6AQAAeqNzSgaJEW8ixKACFBQiOORFishd5S4Qz7WkGyAvA0LNo/wTMQ4S6a5NkeaLagHp/t9Zbk9B6ga2UTgMBMhrC0rtyMirxcWjDCX8+hXQRF5Eex8lXYCu4V7H7HyTvSBPuK29LvIW3aFHvmqxw17hbJBndu67nAhdmxNNZ7r7wuqF861oo9dVhzLHYbhiBjPUmuOr5x22PV8HNtU3a15bH/pTOp/86mPMTWdWmmsO40hy/cFHprjRPILbrZqtt5zsZ46U6d+ODU2pGvwyvOXyIwQ4rSrPcBKcgmUw6Dtq/GBqlVzS9wfKc5RsbjAvn2anQyRSLhdS2ClIRGBc7knewLNuoBXxNrPFq3lPzdt5uXs=~-1~-1~-1; ak_bmsc=DD61DFF3B5C9D1B3E4463FEA8F6BDEC3~000000000000000000000000000000~YAAQT/1VvtC4hLh6AQAAeqNzSgzQJDKMApzD4ibQ2yO5D+QCMRHgTZRmSgabRaqtAeQTyqfPc0D1k3m0S66Jr5kvkwDl1rr1NNCyBLA+jZ83hwbE3Oq2KmOponQVKwsCHqbtQVS7W9Ne7/8kmLznO6z2fbKXtMG8Zntc+aeqY4eJ46PIzSdQPjrIoFu5zqPAOEbnSa99LDEcuJpIErezw5E+EDrbrh8n0OnL5xHzyiyTMYrq9uPKMfzzpM4NDUovIBvvN0TwGcDU0b6Ju+UlF9cqiMUhMaoLZCXw+RcFF/4aAhpstC8h5gJa4BCk/P7EIeBpOFJg9nKgWeqiP6Hkhh46mn3XN67SPHCt4/3iyVYumSCtiKryOQktUcVzkEO9V30=; bm_sz=972FA142E752B8D15050CD920326B68B~YAAQT/1VvtG4hLh6AQAAeqNzSgzXXX/95f+VvKgIwgtfU2OQW+ZMBBTicVhdB7msgrQ1jZ+P5pI1kwmpg3hmAD/29FxFdJTtw6yQTmmoLL8J2d2ZJj6JryxZIjM1uqDkZ7gy1mIP8kKwn61leSzqsZvRD+Zc5wYav5rroxMeNcFT0InjGA+juZx8ZtWfZ1PI5fD2iK1fDhUoZxcLAHJc5ALWycjN/fqV8WpnA+YJKNJVr7ePQncd0aNN3tLJGptKK49ts8dEtjYh2GbwUhuRRO5NQJCGvdpcpdjhTtruOEjQgrgevMA7naI=~3491394~3425845',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'referer': 'https://www.stradivarius.com/'}
        session.headers.update(headers)
        if not endpoints:
            res = self.session.get('https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category').json()
            for _type in res['categories'][0]['subcategories']:
                if any(t == _type['name'] for t in ['Nuevo']):
                    endpoint = {'category':_type['name'],'subcategory': _type['name'], 'id': _type['id']}
                    if not endpoint in endpoints:
                        endpoints.append(endpoint)
                elif any(t == _type['name'] for t in ['Ropa']):
                    for category in _type['subcategories'][0]['subcategories']:
                        for subcategory in category['subcategories']:
                            if not subcategory['name'] == 'Ver todo':
                                endpoint = {'category':category['name'],'subcategory': subcategory['name'], 'id': subcategory['id']}
                                if not endpoint in endpoints:
                                    endpoints.append(endpoint)
                elif any(t == _type['name'] for t in ['Sport', 'Zapatos','Accesorios']) and _type['subcategories']:
                    for subcategory in _type['subcategories'][0]['subcategories']:
                        if not any(t == subcategory['name'] for t in ['Ver todo', 'Todos']):
                            endpoint = {'category':_type['name'],'subcategory': subcategory['name'], 'id': subcategory['id']}
                            if not endpoint in endpoints:
                                endpoints.append(endpoint)
                elif _type['name'] == 'Pijamas':
                    for subcategory in _type['subcategories']:
                        if not subcategory['name'] == 'Ver todo':
                            endpoint = {'category':_type['name'],'subcategory': subcategory['name'], 'id': subcategory['id']}
                            if not endpoint in endpoints:
                                endpoints.append(endpoint)
                elif _type['name'] == 'Rebajas':
                    for _sale in _type['subcategories']:
                        for category in _sale['subcategories']:
                            for subcategory in category['subcategories']:
                                if not subcategory['name'] == 'Ver todo':
                                    endpoint = {'category':category['name'],'subcategory': subcategory['name'], 'id': subcategory['id']}
                                    if not endpoint in endpoints:
                                        endpoints.append(endpoint)
            print(endpoints)
        image_formats = ('image/png', 'image/jpeg', 'image/jpg')
        open('./Database/LogsSTR.txt','w').close()
        for endpoint in endpoints:
            logs = open('./Database/LogsSTR.txt','a')
            headers = session.headers
            res = session.get(endpoint[1]).json()
            logs.write(f'{datetime.now(tz).hour}:{datetime.now(tz).minute}   -   {len(res["products"])} productos  -  {endpoint[0]}\n')
            logs.close()
            for product in res['products']:
                try:
                    ref = f'{product["detail"]["displayReference"]}'
                    category = product['detail']['familyInfo']['familyName']
                    subcategory = product['detail']['subfamilyInfo']['subFamilyName']
                    prod_id = product['id']
                    try:
                        cat_id = product['relatedCategories'][0]['id']
                    except:
                        cat_id = '12345'
                    try:
                        product = product['bundleProductSummaries'][0]
                    except:
                        pass
                    name = product['name']
                    product = product['detail']
                    description = product['description']
                    price_now = int(product['colors'][0]['sizes'][0]['price'])/100
                    try:
                        price_bfr = int(product['colors'][0]['sizes'][0]['oldPrice'])/100
                        sale = True
                    except:
                        price_bfr = price_now
                        sale = False
                    url = f'{endpoint[0][:endpoint[0].index("-c")]}/{name.lower().replace(" ","-")}-c{cat_id}p{prod_id}.html'
                    allSizes = []
                    colors = []
                    for color in product['colors']:
                        sizes = []
                        if color['image']:
                            image = f'https://static.e-stradivarius.net/5/photos3{color["image"]["url"]}_3_1_5.jpg?t={color["image"]["timestamp"]}'
                            colors.append(image)
                        for size in color['sizes']:
                            stock = ''
                            if 'visibilityValue' in size and not size['visibilityValue'] == 'SHOW':
                                stock = '(AGOTADO)'
                            sizes.append(f'{size["name"]} {stock}')
                        allSizes.append(sizes)
                    allImages = []
                    item = Item(brand,name,ref,description,price_bfr,[price_now],0,allImages,url,allSizes,colors,category,category,subcategory,subcategory,sale,'Mujer')
                    extra = product['xmedia']
                    optional_images = []
                    for media in product["xmedia"]:
                        color = []
                        for i in media["xmediaItems"][0]["medias"]:
                            image = f'https://static.e-stradivarius.net/5/photos3{media["path"]}/{i["idMedia"]}2.jpg?t={i["timestamp"]}'
                            color.append(image)
                        optional_images.append(color)
                    image = ''
                    for color in optional_images:
                        for i in color:
                            if not image:
                                r = requests.head(i)
                                if r.headers["content-type"] in image_formats:
                                    image = i
                    found = db.contains(url, image,sync=True)
                    if found:
                        item.allImages = found['allImages']
                    else:
                        for color in optional_images:
                            images = []
                            for image in color:
                                if len(optional_images)==1 or len(images)<2:
                                    r = requests.head(image)
                                    if r.headers["content-type"] in image_formats:
                                        images.append(image)
                            allImages.append(images)
                        item.allImages = allImages
                        db.add(item, sync=True)
                        logs = open('./Database/LogsSTR.txt','a')
                        logs.write(f'    + {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {name}\n')
                        logs.close()
                except Exception as e:
                    print(e)
            sleep(uniform(120,300))
            session = requests.session()
            session.headers.update(headers)


# Main Code
# ScrapStradivarius()
# mouse = webdriver.ActionChains(self.driver)
# mouse.move_to_element(self.driver.find_element_by_xpath('.//div[@class="child-center-parent sidebar-close col-xs-2"]')).click()