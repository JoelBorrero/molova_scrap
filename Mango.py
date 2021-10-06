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
    endpoints = ast.literal_eval(open('./Files/Settings.json','r').read())[brand]['endpoints']
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
                    endpoints.append([category, endpoint])
                    if 'destacados/nuevo' in category:
                        new = endpoint
    driver.quit()
    settings = ast.literal_eval(open('./Files/Settings.json','r').read())
    settings[brand]['endpoints'] = endpoints
    settings[brand]['endpoint'] = new if new else endpoints[0][1]
    with open('./Files/Settings.json','w') as s:
        s.write(str(settings).replace("'",'"'))


class APICrawler:
    def __init__(self, endpoints=endpoints):
        tz = pytz.timezone('America/Bogota')
        filename = './Files/LogsMNG.txt'
        with open(filename, 'w') as logs:
            logs.write(f'··········{datetime.now(tz).month} - {datetime.now(tz).day}··········\n')
        for endpoint in endpoints:
            with open(filename, 'a') as logs:
                logs.write(f'{datetime.now(tz).hour}:{datetime.now(tz).minute}   -   {endpoint[0]}\n')
                pageNum = 1
                try:
                    while pageNum:
                        response = requests.get(endpoint[1]+str(pageNum))
                        if response.status_code == 200:
                            response = response.json()
                            if response['lastPage'] or pageNum == 5:
                                pageNum = 0
                            else:
                                pageNum += 1
                            category = response['titleh1']
                            garments = response['groups'][0]['garments']
                            logs.write(f'    {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {len(garments)} products. (Page {pageNum})\n')
                            for item in garments:
                                it = garments[item]
                                all_images, all_sizes, colors = [], [], []
                                for color in it['colors']:
                                    images = []
                                    sizes = []
                                    for image in color['images']:
                                        images.append(image['img1Src'])
                                    for size in color['sizes']:
                                        sizes.append(size['label']+('(AGOTADO)' if size['stock'] == 0 else ''))
                                    all_images.append(images)
                                    all_sizes.append(sizes)
                                    colors.append(color['iconUrl'].replace(' ',''))
                                # if not all([all(['(AGOTADO)' in size for size in sizes]) for sizes in all_sizes]):
                                all_images.reverse()#I don't know why
                                name = it['shortDescription']
                                db.add(Item(brand, name, it['garmentId'], name, it['price']['crossedOutPrices'], [it['price']['salePrice']], it['price']['discountRate'], all_images, 'https://shop.mango.com'+it['colors'][0]['linkAnchor'], all_sizes, colors, category, category, category, category, 'Mujer'))
                                logs.write(f'      + {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {name}\n')
                                # else:
                                #     logs.write(f'X {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {name} SIN STOCK\n')
                        sleep(randint(30, 120))
                except Exception as e:
                    print('Error in Mango', e)


# ScrapMango()
