import os
import ast
import requests
from random import randint
from datetime import datetime
import pytz
from time import sleep

from selenium import webdriver

from Item import Item
from Database import Database

brand = 'Zara'
db = Database(brand)
tz = pytz.timezone('America/Bogota')
xpaths = {
    'categories': './/ul[@class="layout-categories__container"]/li[position()=2]/ul/li/ul/li/a',
    'color':'.//p[contains(@class,"product-detail-selected-color")]',
    'colorsBtn': './/ul[contains(@class,"-color-selector__colors")]/li/button',
    'coming': '',
    'description': './/div[@class="expandable-text__inner-content"]/p',
    'discount': './/div[@class="product-detail-info__price-amount price"]//span[@class="price__discount-percentage"]',
    'elems': './/section[@class="product-grid"]/ul/li/ul/li[not(contains(@class,"seo"))][.//span[@class="price__amount-current"] and .//a]',
    'href':'.//a',
    'fast_discount': './/div[@class="product-grid-product-info__tag"]/span',
    'fast_image': './/img[not(contains(@src,"watermark"))]',
    'fast_priceBfr':'.//span[@class="price__amount price__amount--old"]',
    'fast_priceNow':'.//span[@class="price__amount-current"]',
    'imgs': './/div[@class="media__wrapper media__wrapper--fill media__wrapper--force-height"]/picture/img[@class="media-image__image media__wrapper--media"]',
    'name': './/h1[@class="product-detail-info__name"]',
    'priceBfr': './/div[@class="product-detail-info__price-amount price"]//span[@class="price__amount price__amount--old" or @class="price__amount-current"]',
    'priceNow': './/div[@class="product-detail-info__price-amount price"]//span[@class="price__amount-current-wrapper"]',
    'ref':'.//p[contains(@class,"product-detail-sel")]',
    'sale': '',
    'sizesTags': './/div[@class="product-detail-info product-detail-view__product-info"]//ul[@class="product-detail-size-selector__size-list"]/li',
    'subcategory': './/span[@class="category-topbar-related-categories__category-name category-topbar-related-categories__category-name--selected"]',
    'subCats':'.//li[@class="variable-width-carousel__item"]/a/div/span',
    'thumbnails': './/ul[@class="product-detail-images-thumbnails product-detail-images__thumbnails"]/li/button',
}
try:
    endpoints = ast.literal_eval(open('./Files/Settings.json','r').read())[brand]['endpoints']
except:
    endpoints = []


class ScrapZara:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.set_page_load_timeout(30)
        self.sale = False
        self.driver.maximize_window()
        self.driver.get('https://www.zara.com/co/')
        sleep(3)
        try:
            self.driver.find_element_by_xpath('.//button[@class="modal__close-button"]').click()
            sleep(2)
            self.driver.find_element_by_xpath('.//button[@class="modal__close-button"]').click()
        except:
            pass
        cats=[[],[]]
        for cat in self.driver.find_elements_by_xpath(xpaths['categories']):
            c = cat.get_attribute('innerText').capitalize()
            cats[0].append(c)
            cats[1].append(cat.get_attribute('href'))
        cats[0].reverse()
        cats[1].reverse()
        for i in range(len(cats[0])):
            self.category = cats[0][i]
            self.originalCategory = self.category
            if 'mujer' in cats[1][i] or 'woman' in cats[1][i]:
                self.gender = 'Mujer'
                self.scrap_category(cats[1][i])
            else:
                self.gender = 'Hombre'
            # self.scrap_category(cats[1][i])

    def scrap_category(self, url):
        self.driver.get(url)
        try:
            self.subcategory = self.driver.find_element_by_xpath(xpaths['subcategory']).text.capitalize()
        except:
            self.subcategory = self.category
        subcats = self.driver.find_elements_by_xpath(xpaths['subCats'])
        if subcats:
            for s in range(len(subcats)):
                if subcats[s].text.lower() != 'ver todo':
                    try:
                        subcats[s].click()
                        sleep(5)
                        self.subcategory = self.driver.find_element_by_xpath(xpaths['subcategory']).text.capitalize()
                        self.scrap_subcategory()
                    except:
                        # try:
                        self.driver.find_element_by_xpath('.//button[@class="variable-width-carousel__arrow variable-width-carousel__arrow--right"]').click()
                        sleep(1)
                        subcats[s].click()
                        sleep(5)
                        self.subcategory = self.driver.find_element_by_xpath(xpaths['subcategory']).text.capitalize()
                        self.scrap_subcategory()
                        # except:
                        #     print('Never click')
                subcats = self.driver.find_elements_by_xpath(xpaths['subCats'])
        else:
            self.scrap_subcategory()
            
    def scrap_subcategory(self):
        self.originalSubcategory = self.subcategory
        elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(3)
        loading = True
        while loading:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(3)
            loading = len(elems) < len(self.driver.find_elements_by_xpath(xpaths['elems']))
            elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        while elems:
            elem = elems.pop()
            self.driver.execute_script('arguments[0].scrollIntoView();', elem)
            url = elem.find_element_by_xpath(xpaths['href']).get_attribute('href')
            try:
                image = elem.find_element_by_xpath(xpaths['fast_image']).get_attribute('src')
            except:
                image = ''
            if db.contains(url, image):
                db.update_product(elem, url, xpaths)
            else:
                self.scrap_product(url)


    def scrap_product(self, url):
        mouse = webdriver.ActionChains(self.driver)
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            name = self.driver.find_element_by_xpath(xpaths['name']).text.capitalize()
            ref = self.driver.find_element_by_xpath(xpaths['ref']).text
            ref = ref[ref.index(' | ')+3:]
            try:
                description = self.driver.find_element_by_xpath(xpaths['description']).text.capitalize()
            except:
                description = ''
            priceNow = self.driver.find_element_by_xpath(xpaths['priceNow']).text
            try:
                priceBfr = self.driver.find_element_by_xpath(xpaths['priceBfr']).text
                discount = self.driver.find_element_by_xpath(xpaths['discount']).get_attribute('innerText')
            except:
                priceBfr = priceNow
                discount = 0
            colorsBtn = self.driver.find_elements_by_xpath(xpaths['colorsBtn'])
            colors = []
            allSizes = []
            allImages = []
            if len(colorsBtn) == 0:
                color = self.driver.find_element_by_xpath(xpaths['color'])
                colors.append(color.text.replace('Color: ', '').replace('"', '').capitalize())
                sizes = []
                for t in self.driver.find_elements_by_xpath(xpaths['sizesTags']):
                    if 'disabled' in t.get_attribute('class'):
                        sizes.append('{}(Agotado)'.format(t.find_element_by_xpath('./div/div/span').get_attribute('innerText')))
                    else:
                        sizes.append(t.find_element_by_xpath('./div/div/span').get_attribute('innerText'))
                allSizes.append(sizes)
                images = []
                thumbnails = self.driver.find_elements_by_xpath(xpaths['thumbnails'])
                for i in range(len(thumbnails)):
                    mouse.move_to_element(thumbnails[i]).perform()
                    thumbnails[i].click()
                for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                    if not 'transparent-background' in i.get_attribute('src'):
                        images.append(i.get_attribute('src'))
                allImages.append(images)
            for c in range(len(colorsBtn)):
                colorsBtn[c].click()
                sizes = []
                while not self.driver.find_elements_by_xpath('.//ul[contains(@id,"product-size-selector-product-detail-info")]/li'):
                    sleep(0.1)
                for t in self.driver.find_elements_by_xpath('.//ul[contains(@id,"product-size-selector-product-detail-info")]/li'):
                    if 'disabled' in t.get_attribute('class'):
                        sizes.append('{}(Agotado)'.format(t.find_element_by_xpath('./div/div/span').get_attribute('innerText')))
                    else:
                        sizes.append(t.find_element_by_xpath('./div/div/span').get_attribute('innerText'))
                allSizes.append(sizes)
                images = []
                thumbnails = self.driver.find_elements_by_xpath(xpaths['thumbnails'])
                for i in range(len(thumbnails)):
                    mouse.move_to_element(thumbnails[i]).perform()
                    thumbnails[i].click()
                for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                    if not 'transparent-background' in i.get_attribute('src'):
                        images.append(i.get_attribute('src'))
                        print(i.get_attribute('src'))
                allImages.append(images)
                colors.append(colorsBtn[c].get_attribute('innerText').replace('Color: ', '').replace('"', '').capitalize())
                colorsBtn = self.driver.find_elements_by_xpath('.//ul[@class="product-detail-info-color-selector__colors"]/li/button')
            db.add(Item(brand,name,ref,description,priceBfr,[priceNow],discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory, self.gender))
        except Exception as e:
            i = 0
            print('Item saltado\n',url,e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


def scrap_for_links():
    driver = webdriver.Chrome('./chromedriver')
    driver.set_page_load_timeout(30)
    driver.maximize_window()
    driver.get('https://www.zara.com/co/')
    try:
        driver.find_element_by_xpath('.//button[@class="modal__close-button"]').click()
        sleep(2)
        driver.find_element_by_xpath('.//button[@class="modal__close-button"]').click()
    except:
        pass
    main_categories = []
    for c in driver.find_elements_by_xpath(xpaths['categories']):
        main_categories.append(c.get_attribute('href'))
    get_network = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;'
    endpoints.clear()
    news = ''
    for c in main_categories:
        if c:
            driver.get(c)
            sleep(1)
            netData = driver.execute_script(get_network)
            for i in netData:
                if 'products?ajax' in i['name']:
                    endpoints.append([c,i['name']])
                    if 'nuevo-' in c:
                        news = i['name']
    driver.quit()
    settings = ast.literal_eval(open('./Files/Settings.json','r').read())
    settings[brand]['endpoints'] = endpoints
    settings[brand]['endpoint'] = news if news else endpoints[0][1]
    with open('./Files/Settings.json','w') as s:
        s.write(str(settings).replace("'",'"'))



class APICrawler:
    def __init__(self, endpoints=endpoints):
        session = requests.session()
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'cookie': 'ITXSESSIONID=d458e4b17f001e37dfdd0cc93fbe1717; web_version=STANDARD; bm_sz=B77396026A92E8F97FA258393551A02E~YAAQpKpLaP3Jm7R6AQAAMbyEvg2KTcnl6zbnIQp+bZr8QZF8eXTyts74BzbwCO5yOYGfgrQ1IK/ZtgBxEIdaxz/4vh4DW3DjZOvD6jMhLg7HWKxSEJLwRG3QE9en2at6n104IgL8ncgIML9rNJfv9bzJoKScK+FbZnG9Xav64FI9U850vPuzCcC2Q7yluiPX1McNYw0glOBo7TH6dO5feI2rFAWAJJfHv6Y2eQ6gYu46OZ7vOanrBwTi4HaeVptV80R+3gLetroqBfLaWXZIIT82hBO90y27hL8JeHD/HtE0~3424833~4273222; _abck=AD1BE4EBB69FA500FE0C71CB433A60B0~0~YAAQpKpLaAPKm7R6AQAAj8GEvgZ+SRGl6rrPLN5AeYGCRe76FBuhKFLzvcf3qD+YdOCRYAq2AO4JgUfWq00iE7KWe9B8TeKUqodFqzD/yAoJrN+LvAfwmmP5mO+hPcndGJYxcSWBTUZRrzFyR8labOPBk04SMr6ie4QMrOtjwfo8W8vG9PDex8FGoZhZqcE4Qu10CbBlOpzcumdc0ka6X2L/D2XMfq19EyBgvRiWSKHCHZOC6R4SxI8z1VrDxGvpcdxDNSq+UzOWpjPuV8xRJwQfoKfItmWWPzEcPn3OF2mwQGhHy6JUaE/mIF1ldde8qpRz38KFsrLYX2n+Htlim5tgX0gLSo1UhSmYgVDXx/KbM2Yr0l5ImcUGgNE2lCZsj6hJ5tQT12ARz8zv/FBvQZxCmNiFaw==~-1~-1~-1; ak_bmsc=8329DA2709C86864C6E40D3ACBA821AE~000000000000000000000000000000~YAAQpKpLaAvKm7R6AQAAP8WEvg33e6w414subhHXC3mgw6uB3YZvjS22aPHbCCOR2laB3AF2hINX/nG2ud2aPU/v5/kJFsIbuoaI5WTCKYiqIyJEks63rvazFKn4okA8r5u/Q0pvGUpPz/L8GdmTOHxrU7cvHqltA5MS/nD0C1Ctt6TXz0M1kmZKBOEJHmlPH1mQPoNiZQVieRSO4+bk4Im9ml5yO691ogvDxw//dHwUd4xvWylRyyHAqTl89Mbar93V2xmKl/ANvdzPRwtzdFxVameqNjlL+nYLPAlPNxsLfKPKcKjHhl45G5iAtcMbc5BahKLAwQ4QuutHfVnFWaWANAO7UH1v7h1kOT5LqM8L+bTryXq0xWUSLpL/R6D++Uaz1J69mEfisXiH5VVeyHtXiInPxYiucKayF5bLUE60rCT9fSsVfb8zxwRkdaPx4AQ+Vdhcc/X6ujcubVnBZyyrh4j3OhxF+ZmUsOcrZmEr9wrTpxpN/w==; rid=61e5ec44-e21e-4a15-a356-817a5015c536; vwr_global=1.1.1630988978.b8630a30-29c8-4f68-a346-56eeff82262b.1630988978..M4EHYfBDQijUPEKmwTyNXh4yy6_bS2cOX-QOKMWkhow; storepath=co%2Fes; cart-was-updated-in-standard=true; rskxRunCookie=0; rCookie=jo27kadi1hlmxxaul4r3kt9kq6n1; chin={"status":"chat-status:not_connected","isChatAttended":false,"privacyAccepted":false,"email":"","userJid":"","uiCurrentView":"view:hidden","timeShowInteractiveChat":0,"compatMode":true,"businessKind":"online"}; lastRskxRun=1630988990053; _ga=GA1.2.1818226498.1630988991; _gid=GA1.2.237491462.1630988991; _fbp=fb.1.1630988991038.1662346990; _gat_UA-18083935-1=1; OptanonConsent=isIABGlobal=false&datestamp=Mon+Sep+06+2021+23%3A29%3A51+GMT-0500+(Colombia+Standard+Time)&version=6.8.0&hosts=&consentId=a9608d84-85af-48dd-b839-cfa5e1d8d766&interactionCount=1&landingPath=https%3A%2F%2Fwww.zara.com%2Fco%2Fes%2Fmujer-nuevo-l1180.html%3Fv1%3D1881787&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1; RT="z=1&dm=zara.com&si=38791a9a-8027-4374-94b3-e222789fe077&ss=kt9kq31v&sl=4&tt=emy&bcn=%2F%2F17c8edc7.akstat.io%2F&ld=dz3&ul=y6f&hd=ycs"; _ga_D8SW45BC2Z=GS1.1.1630988990.1.0.1630989019.31',
            'pragma': 'no-cache',
            'referer': 'https://www.zara.com/co/es/mujer-nuevo-l1180.html?v1=1881787',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'][randint(0, 4)]}
        session.headers.update(headers)
        filename = './Files/LogsZARA.txt'
        with open(filename, 'w') as logs:
            logs.write(f'··········{datetime.now(tz).month} - {datetime.now(tz).day}··········\n')
        for endpoint in endpoints:
            products = session.get(endpoint[1]).json()['productGroups'][0]['elements']
            with open(filename, 'a') as logs:
                logs.write(f'{datetime.now(tz).hour}:{datetime.now(tz).minute}   -   {len(products)} productos  -  {endpoint[0]}\n')
            for product in products:
                with open(filename, 'a') as logs:
                    try:
                        # layout = product['layout'] #1G
                        product = product['commercialComponents'][0]
                        name = product['name']
                        description = product['description']
                        price_before = product['price']/100
                        try:
                            price_now = product['price_discount']  # TODO
                            discount = product['discount']
                        except KeyError:
                            price_now = price_before
                            discount = 0
                        url = f'https://www.zara.com/co/es/{product["seo"]["keyword"]}-p{product["seo"]["seoProductId"]}.html'
                        category = product['familyName']
                        subcategory = product['subfamilyName']
                        product = product['detail']
                        ref = product['displayReference']
                        colors, all_images, all_sizes = [], [], []
                        for color in product['colors']:
                            colors.append(color['name'])
                            images, sizes = [], []
                            for image in color['xmedia']:
                                images.append(f'https://static.zara.net/photos//{image["path"]}/w/563/{image["name"]}.jpg?ts={image["timestamp"]}')
                            all_images.append(images)
                        # TODO Verify no-stock
                        # if not all([all(['(AGOTADO)' in size for size in sizes]) for sizes in all_sizes]):
                        item = Item(brand,name,ref,description,price_before,[price_now],discount,all_images,url,all_sizes,colors,category,category,subcategory,subcategory,'Mujer')
                        db.add(item)
                        logs.write(f'    + {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {name}\n')
                        # else:
                        #     logs.write(f'X {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {name} {url} SIN STOCK\n')
                    except Exception as e:
                        logs.write(f'X {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {e}\n')
                        print(e)
            headers = session.headers
            sleep(randint(30, 120))
            session = requests.session()
            session.headers.update(headers)
