import ast
import pytz
import requests
from time import sleep
from random import randint
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Item import Item
from Database import Database

brand = 'Pull & Bear'
db = Database(brand)
tz = pytz.timezone('America/Bogota')
xpaths={
    'categories':'.//ul[@class="product-categories"]/li[not(contains(@class,"has-subitems") or contains(@class,"hidden"))]/a|.//ul[@class="product-categories"]/li/ul/li[not(contains(@class,"hidden"))]/a',
    'categoriesSale':'.//ul[@class="product-categories"]/li[contains(@class,"sale")]/ul/li/a',
    'colorsBtn':'.//div[@class="c-product-info--header"]/div[contains(@class,"product-card-color-selector")]/div/div/div/img',
    'description':'.//span[@class="c-product-info--description-text"]',
    'discount':'./../..//div[@class="product-price--price product-price--price-discount"]',
    'elems':'.//div[contains(@class,"c-tile c-tile--product")][div/a]',
    'fast_discount': './div/div/div[@class="discount"]',
    'fast_image': './div/a/div/div/figure/img',
    'fast_priceBfr': './/div[contains(@class,"product-price--price-old")]',
    'fast_priceNow': './/div[contains(@class,"product-price--price")]',
    'href':'./div/a',
    'imgs':'.//div[@id="product-grid"]/div/div/figure/img',
    'name':'.//h1[@class="title"]',
    'priceBfr':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div[contains(@class,"price")]/span',
    'priceNow':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div[@class="sale"]/span',
    'priceNow2':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div/span',
    'ref':'.//span[@class="c-product-info--description-header-reference"]',
    'sizesTags':'.//div[@class="c-product-info--size"]/div/div/div[@class="product-card-size-selector--dropdown-sizes"]/div',
    'subCats':'.//div[starts-with(@class,"carrousel-filters")]/div/div/div/div',
    'subCats2':'.//div[@class="category-badges-list"]/button[not(@value="Ver todo")][span]'}
try:
    with open('./Files/Settings.json','r') as settings:
        endpoints = ast.literal_eval(settings.read())[brand]['endpoints']
except:
    endpoints = []


class ScrapPullAndBear:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.set_page_load_timeout(30)
        self.driver.maximize_window()
        self.gender = 'Mujer'
        self.scrapGender('https://www.pullandbear.com/co/mujer-n6417')
        self.driver.quit()
        
    def scrapGender(self, url):
        self.sale = False
        self.driver.get(url)
        categories = [self.driver.find_elements_by_xpath(xpaths['categories']),[]]
        if not categories[0]:
            sleep(5)
            categories = [self.driver.find_elements_by_xpath(xpaths['categories']),[]]
        for c in categories[0]:
            cat = c.get_attribute('innerText').replace('\n', '')
            while '  ' in cat:
                cat = cat.replace('  ', ' ')
            categories[0][categories[0].index(c)] = cat.strip()
            categories[1].append(c.get_attribute('href'))
        for c in categories[0]:
            self.category = c
            self.originalCategory = c
            self.scrapCategory(categories[1][categories[0].index(c)])

    def scrapCategory(self, url):
        self.driver.get(url)
        subCats = self.driver.find_elements_by_xpath(xpaths['subCats'])
        type = 1
        if not subCats:
            sleep(5)
            subCats = self.driver.find_elements_by_xpath(xpaths['subCats'])
            if not subCats:
                subCats = self.driver.find_elements_by_xpath(xpaths['subCats2'])
                if subCats:
                    print(url,'type2')
                    type = 2#Text buttons
                    for button in subCats:
                        self.driver.find_element_by_xpath('.//body').send_keys(Keys.HOME)
                        sleep(1)
                        button.click()
                        sleep(3)
                        self.subcategory = button.find_element_by_xpath('./span').text
                        self.originalSubcategory = self.subcategory
                        self.scrapSubcategory()
                else:
                    type = 3
        if subCats and type == 1:
            for i in range(len(subCats)):
                if not 'Ver Todo' in subCats[i].get_attribute('innerText'):
                    subCats = self.driver.find_elements_by_xpath(xpaths['subCats'])
                    self.subcategory = subCats[i].find_element_by_xpath('.//p').text
                    if not self.subcategory:
                        self.subcategory = (subCats[i].find_element_by_xpath('.//p').get_attribute('innerText'))
                    # self.driver.execute_script('arguments[0].scrollIntoView();', subCats[i])
                    self.driver.find_element_by_xpath('.//body').send_keys(Keys.HOME)
                    try:
                        subCats[i].find_element_by_xpath('./div').click()
                    except:
                        self.driver.find_element_by_xpath('.//button[@class="flickity-button flickity-custom-prev-next-button next icon icon-flickity-next"]').click()
                        sleep(1)
                        try:
                            subCats[i].find_element_by_xpath('./div').click()
                        except:
                            self.driver.find_element_by_xpath('.//button[@class="flickity-button flickity-custom-prev-next-button next icon icon-flickity-next"]').click()
                            sleep(1)
                            try:
                                subCats[i].find_element_by_xpath('./div').click()
                            except:
                                self.driver.find_element_by_xpath('.//button[@class="flickity-button flickity-custom-prev-next-button next icon icon-flickity-next"]').click()
                                sleep(1)
                                subCats[i].find_element_by_xpath('./div').click()
                    sleep(3)
                    self.originalSubcategory = self.subcategory
                    self.scrapSubcategory()
        elif type == 3:
            self.subcategory = self.category
            self.originalSubcategory = self.subcategory
            self.scrapSubcategory()

    def scrapSubcategory(self, url=''):
        if url:
            self.driver.get(url)
            sleep(5)
        loading = True
        elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        while loading:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_UP)
            self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_UP)
            sleep(5)
            loading = len(elems) < len(self.driver.find_elements_by_xpath(xpaths['elems']))
            elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        for elem in elems:
            self.driver.execute_script('arguments[0].scrollIntoView();', elem)
            url = elem.find_element_by_xpath(xpaths['href']).get_attribute('href')
            try:
                image = elem.find_element_by_xpath(xpaths['fast_image']).get_attribute('src')
            except:
                image = ''
            if db.contains(url, image):
                db.update_product(elem, url, xpaths)
            else:
                try:
                    discount = elem.find_element_by_xpath(xpaths['fast_discount']).text
                except:
                    discount = 0
                self.scrapProduct(url, discount)

    def scrapProduct(self, url, discount):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            try:
                name = self.driver.find_element_by_xpath(xpaths['name']).text
            except:
                sleep(3)
                name = self.driver.find_element_by_xpath(xpaths['name']).text
            ref = self.driver.find_element_by_xpath(xpaths['ref']).text
            description = self.driver.find_element_by_xpath(xpaths['description']).text
            try:
                priceNow = self.driver.find_element_by_xpath(xpaths['priceNow']).text
            except:
                priceNow = self.driver.find_element_by_xpath(xpaths['priceNow2']).text
            try:
                priceBfr = self.driver.find_element_by_xpath(xpaths['priceBfr']).text
            except:
                priceBfr = priceNow
            colorsBtn = self.driver.find_elements_by_xpath(xpaths['colorsBtn'])
            colors = []
            allSizes = []
            allImages = []
            for c in colorsBtn:
                try:
                    c.click()
                    colors.append(c.get_attribute('src'))
                    sizes = []
                    sizesTags = self.driver.find_elements_by_xpath(xpaths['sizesTags'])
                    for s in sizesTags:
                        if 'disabled' in s.get_attribute('class'):
                            sizes.append('{}(AGOTADO)'.format(s.get_attribute('innerText')))
                        else:
                            sizes.append(s.get_attribute('innerText'))
                    if not sizesTags:
                        sizes = ['Única']
                    allSizes.append(sizes)
                    images = []
                    imgs = self.driver.find_elements_by_xpath(xpaths['imgs'])
                    for i in range(len(imgs)):
                        while not imgs[i].get_attribute('src'):
                            self.driver.execute_script('arguments[0].scrollIntoView();', imgs[i])
                            imgs = self.driver.find_elements_by_xpath(xpaths['imgs'])
                            sleep(1)
                        images.append(imgs[i].get_attribute('src'))
                    allImages.append(images)
                except:
                    pass
            db.add(Item(brand,name,ref,description,priceBfr,priceNow,discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale,self.gender))
        except Exception as e:
           print("Item saltado:",e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

def scrap_for_links():
    driver = webdriver.Chrome('./chromedriver')
    driver.set_page_load_timeout(30)
    driver.maximize_window()
    driver.get('https://www.pullandbear.com/co/mujer-n6417')
    sleep(2)
    try:
        driver.find_element_by_xpath('.//button[@class="onetrust-close-btn-handler banner-close-button ot-close-icon"]').click()
    except:
        print('Something not dismissed')
    endpoints.clear()
    categories = []
    for i in driver.find_elements_by_xpath(xpaths['categories']):
        categories.append(i.get_attribute('href'))
    look_network = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;'
    new = ''
    for category in categories:
        if 'mujer' in category:
            try:
                driver.get(category)
                endpoint = ''
                timeout = 1
                while not endpoint and timeout < 5:
                    sleep(1)
                    netData = driver.execute_script(look_network)
                    for i in netData:
                        if '/product?language' in i['name']:
                            endpoint = i['name']
                            if not endpoint in str(endpoints):
                                endpoints.append([category, endpoint])
                                if 'novedades' in category:
                                    new = endpoint.replace('showProducts=false', 'showProducts=true')
                    if not endpoint:
                        timeout += 1
            except Exception as e:
                print(e)
    driver.quit()
    settings = ast.literal_eval(open('./Files/Settings.json','r').read())
    settings[brand]['endpoints'] = endpoints
    settings[brand]['endpoint'] = new if new else endpoints[0][1]
    with open('./Files/Settings.json','w') as s:
        s.write(str(settings).replace("'",'"'))


class APICrawler:
    def __init__(self, endpoints=endpoints):
        session = requests.session()
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7',
            'content-type': 'application/json',
            'referer': 'https://www.pullandbear.com/',
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
        session.headers.update(headers)
        image_formats = ('image/png', 'image/jpeg', 'image/jpg')
        filename = './Files/LogsPULL.txt'
        with open(filename, 'w') as logs:
            logs.write(f'··········{datetime.now(tz).month} - {datetime.now(tz).day}··········\n')
        pageSize = 25
        for endpoint in endpoints:
            category_id = endpoint[1][endpoint[1].index('/category/') + 10 : endpoint[1].rindex('/')]
            response = session.get(endpoint[1]).json()['productIds']
            with open(filename, 'a') as logs:
                logs.write(f'{datetime.now(tz).hour}:{datetime.now(tz).minute}   -   {len(response)} productos  -  {endpoint[0]}\n')
            for page in range(len(response) // pageSize):
                ids = [id for id in response[page * pageSize : (page + 1) * pageSize]]
                page_endpoint = f'https://www.pullandbear.com/itxrest/3/catalog/store/25009465/20309430/productsArray?productIds={str(ids)[1:-1].replace(", ", "%2C")}&languageId=-5&categoryId={category_id}&appId=1'
                products = session.get(page_endpoint).json()['products']
                for product in products:
                    with open(filename, 'a') as logs:
                        try:
                            if 'productUrl' in product:
                                name = product['name']
                                param = f'&pelement={product["bundleProductSummaries"][0]["productUrlParam"]}' if product['bundleProductSummaries'] and 'productUrlParam' in product['bundleProductSummaries'][0] else ''
                                url = f'https://www.pullandbear.com/co/{product["productUrl"]}?cS={product["mainColorid"]}{param}'
                                if product['bundleProductSummaries']:
                                    product = product['bundleProductSummaries'][0]['detail']
                                else:
                                    product = product['detail']
                                description = product['description'] if product['description'] else product['longDescription']
                                ref = product['displayReference']
                                category = product['familyInfo']['familyName']
                                subcategory = product['subfamilyInfo']['subFamilyName']
                                colors, all_images, all_sizes = [], [], []
                                for color in product['colors']:
                                    colors.append(f'https://static.pullandbear.net/2/photos/{color["image"]["url"]}_1_1_8.jpg?t={color["image"]["timestamp"]}&imwidth=90')
                                    sizes = []
                                    for size in color['sizes']:
                                        stock = '' if size['visibilityValue'] == 'SHOW' else '(AGOTADO)'
                                        sizes.append(size['name'] + stock)
                                    all_sizes.append(sizes)
                                # if not all([all(['(AGOTADO)' in size for size in sizes]) for sizes in all_sizes]):
                                if product['xmedia']:
                                    price_now = [int(product['colors'][0]['sizes'][0]['price']) / 100]
                                    try:
                                        price_before = int(product['colors'][0]['sizes'][0]['oldPrice']) / 100#TODO
                                    except TypeError:
                                        price_before = price_now[0]
                                    for media in product['xmedia']:
                                        images = []
                                        for i in media['xmediaItems'][0]['medias']:
                                            if not '_3_1_' in i['idMedia']:
                                                images.append(f'https://static.pullandbear.net/2/photos/{media["path"]}/{i["idMedia"]}8.jpg?ts={i["timestamp"]}')
                                        all_images.append(images)
                                    item = Item(brand,name,ref,description,price_before,price_now,0,all_images,url,all_sizes,colors,category,category,subcategory,subcategory,'Mujer')
                                    db.add(item)
                                    logs.write(f'    + {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {name}\n')
                                # else:
                                    # logs.write(f'X {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {name} SIN STOCK {url}\n')
                        except Exception as e:
                            print(e)
                            logs.write(f'X {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {e}\n')
            headers = session.headers
            sleep(randint(30, 120))
            session = requests.session()
            session.headers.update(headers)

# Main Code
# ScrapPullAndBear()