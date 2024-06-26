import requests
import ast
from time import sleep
from random import randint
from datetime import datetime
import pytz

from selenium import webdriver

from Item import Item
from Database import Database

brand = 'Mango'
db = Database(brand)
tz = pytz.timezone('America/Bogota')
xpaths={
    'categories':'.//div[@class="section-detail-container section-detail-hidden "]/div/ul[@class="section-detail"]/li[not(contains(@class,"desktop-label-hidden") or contains(@class," label-hidden"))]/a',
    'discount':'.//span[@class="product-discount"]',
    'imgs':'.//div[@id="renderedImages"]//img',
    'name':'.//h1[@itemprop="name"]',
    'priceBfr':'.//span[contains(@class,"product-sale") and not(contains(@class,"discount"))]',
    'priceNow':'.//span[contains(@class,"product-sale")]'}
try:
    endpoints = ast.literal_eval(open('./Files/.settings','r').read())[brand]['endpoints']
except:
    endpoints = []


class ScrapMango:
    def __init__(self):
        if not endpoints:
            self.scrap()
        APICrawler()


def scrap_for_links():
    driver = webdriver.Chrome('./chromedriver')
    driver.set_page_load_timeout(30)
    driver.maximize_window()
    driver.get('https://shop.mango.com/co/mujer')
    sleep(2)
    try:
        driver.find_element_by_id('onetrust-accept-btn-handler').click()
        driver.find_element_by_xpath('.//div[@class="icon closeModal icon__close desktop confirmacionPais"]').click()
    except:
        print('Something not dismissed')
    endpoints.clear()
    categories = []
    for i in driver.find_elements_by_xpath(xpaths['categories']):
        categories.append(i.get_attribute('href'))
    look_network = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;'
    new = ''
    for category in categories:
        driver.get(category)
        netData = driver.execute_script(look_network)
        for i in netData:
            if '/services/productlist/products/CO/she/' in i['name']:
                endpoint = i['name']
                endpoint = endpoint[:endpoint.index('&pageNum=')]
                if not endpoint in str(endpoints):
                    endpoints.append((category, endpoint))
                    if 'destacados/nuevo' in category:
                        new = endpoint
    driver.quit()
    settings = ast.literal_eval(open('./Files/.settings','r').read())
    settings[brand]['endpoints'] = endpoints
    settings[brand]['endpoint'] = new if new else endpoints[0][1]
    with open('./Files/.settings','w') as s:
        s.write(str(settings))


class APICrawler:
    def __init__(self, endpoints=endpoints):
        open('./Files/LogsMNG.txt','w').close()
        tz = pytz.timezone('America/Bogota')
        for endpoint in endpoints:
            logs = open('./Files/LogsMNG.txt','a')
            logs.write(f'{datetime.now(tz).hour}:{datetime.now(tz).minute}   -   {endpoint[0]}\n')
            pageNum = 1
            try:
                while pageNum:
                    response = requests.get(endpoint[1]+str(pageNum))
                    if response.status_code == 200:
                        response = response.json()
                        if response['lastPage']:
                            pageNum = 0
                        else:
                            pageNum += 1
                        self.category = response['titleh1']
                        garments = response['groups'][0]['garments']
                        logs.write(f'    {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {len(garments)} products. (Page {pageNum})\n')
                        for item in garments:
                            it = garments[item]
                            allImages, allSizes, colors = [], [], []
                            for color in it['colors']:
                                images = []
                                sizes = []
                                for image in color['images']:
                                    images.append(image['img1Src'])
                                for size in color['sizes']:
                                    sizes.append(size['label']+('(Agotado)' if size['stock'] == 0 else ''))
                                allImages.append(images)
                                allSizes.append(sizes)
                                colors.append(color['iconUrl'].replace(' ',''))
                            allImages.reverse()#I don't know why
                            db.add(
                                Item(
                                    brand,
                                    it['shortDescription'],
                                    it['garmentId'],
                                    it['shortDescription'],
                                    it['price']['crossedOutPrices'],
                                    [it['price']['salePrice']],
                                    it['price']['discountRate'],
                                    allImages,
                                    'https://shop.mango.com'+it['colors'][0]['linkAnchor'],
                                    allSizes,
                                    colors,
                                    self.category,
                                    self.category,
                                    self.category,
                                    self.category,
                                    False,
                                    'Mujer'))
                            logs.write(f'      + {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {it["shortDescription"]}\n')
                    sleep(randint(30, 120))
            except Exception as e:
                print('Error in Mango', e)
            logs.close()
        # db.close()


# ScrapMango()
