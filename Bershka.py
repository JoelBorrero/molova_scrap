import ast
import pytz
import requests
from time import sleep
from datetime import datetime
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Item import Item
from Database import Database

brand = 'Bershka'
db = Database(brand)
tz = pytz.timezone('America/Bogota')
xpaths = {
    'categories': './/li[@class="sub-menu-item"]/a[not(contains(@href,"total-look")) and not(contains(@href,"join")) and not(contains(@href,"creators")) and not(@aria-label="Ir a Ver Todo")]',
    'colorsBtn': './/ul[@class="swiper-wrapper"]/li/a/span/img',
    'coming': './span/span/span',
    'description': './/section[@class="product-info"]',
    'discount': './/div[contains(@class,"price-elem")]/span[@class="discount-tag"]',
    'elems': './/ul[@class="grid-container"]/li/div/a',
    'fast_discount': './div/div/span',
    'fast_priceBfr':'.//span[contains(@class,"old-price")]',
    'fast_priceNow':'.//div[contains(@class,"price-elem")]/span[contains(@class,"current")]',
    'imgs': './/div/button/span[@class="image-item-wrapper"]/img',
    'name': './/h1[@class="product-title"]',
    'priceBfr': './/span[@class="old-price-elem"]|.//div[@class="top-group"]/div/span[@class="current-price-elem"]',
    'priceNow': './/span[contains(@class,"current-price-elem")]',
    'ref': './/div[@class="product-reference"]',
    'sale': './/ul[@class="sub-menu-container is-active"]/li/a',
    'sizesTags': './/div[@class="sizes-list-detail"]/ul/li/button',
    'subCats': './/div[@class="filter-tag-swiper"]/div/ul/li',
}
try:
    with open('./Files/Settings.json','r') as settings:
        endpoints = ast.literal_eval(settings.read())[brand]['endpoints']
except:
    endpoints = []


class ScrapBershka:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.set_page_load_timeout(30)
        self.driver.maximize_window()
        self.driver.get('https://www.bershka.com/co/')
        self.scrapSale()
        self.scrapCategories()
        self.driver.quit()

    def scrapSale(self):
        self.sale = True
        categories = [[], [], self.driver.find_elements_by_xpath(xpaths['sale'])]
        for c in categories[2]:
            cat = c.get_attribute('innerText').replace('\n', '')
            categories[0].append(cat.strip())
            categories[1].append(c.get_attribute('href'))
        for c in range(len(categories[0])):
            self.category = categories[0][c]
            self.originalCategory = self.category
            if 'hombre' in categories[1][c]:
                self.gender = 'Hombre'
            else:
                self.gender = 'Mujer'
                self.scrapCategory(categories[1][c])
                
    def scrapCategories(self):
        self.sale = False
        categories = [[], [], self.driver.find_elements_by_xpath(xpaths['categories'])]
        for c in categories[2]:
            cat = c.get_attribute('innerText').replace('\n', '').strip()
            categories[0].append(cat)
            categories[1].append(c.get_attribute('href'))
        categories[2].clear()
        for c in range(len(categories[0])):
            self.category = categories[0][c]
            self.originalCategory = categories[0][c]
            if 'hombre' in categories[1][c]:
                self.gender = 'Hombre'
            else:
                self.gender = 'Mujer'
                self.scrapCategory(categories[1][c])

    def scrapCategory(self, url):
        self.driver.get(url)
        sleep(1)
        self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_DOWN)
        subCats = self.driver.find_elements_by_xpath(xpaths['subCats'])
        if not subCats:
            self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_DOWN)
            sleep(5)
            subCats = self.driver.find_elements_by_xpath(xpaths['subCats'])
        if subCats:
            for s in range(len(subCats)):
                if not 'Todas' in subCats[s].get_attribute('innerText'):
                    self.driver.find_element_by_xpath('.//body').send_keys(Keys.HOME)
                    sleep(1)
                    subCats[s].click()
                    self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_DOWN)
                    sleep(1)
                    subCats = self.driver.find_elements_by_xpath(xpaths['subCats'])
                    self.subcategory = subCats[s].get_attribute('innerText')
                    self.originalSubcategory = subCats[s].get_attribute('innerText')
                    self.scrapSubcategory()
        else:
            self.subcategory = self.category
            self.originalSubcategory = self.category
            self.scrapSubcategory()

    def scrapSubcategory(self):
        elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        loading = True
        while loading:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_UP)
            sleep(3)
            loading = len(elems) < len(self.driver.find_elements_by_xpath(xpaths['elems']))
            elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        while elems:
            e = elems.pop()
            self.driver.execute_script('arguments[0].scrollIntoView();', e)
            url = e.get_attribute('href')
            if db.contains(url):
                db.update_product(e, url, xpaths)
            else:
                self.scrapProduct(url)

    def scrapProduct(self, url):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            if not self.driver.find_elements_by_xpath(xpaths['imgs']):
                sleep(1)
            name = self.driver.find_element_by_xpath(xpaths['name']).text
            ref = self.driver.find_element_by_xpath(xpaths['ref']).text
            description = self.driver.find_element_by_xpath(xpaths['description']).text
            priceNow = self.driver.find_element_by_xpath(xpaths['priceNow']).text
            try:
                priceBfr = self.driver.find_element_by_xpath(xpaths['priceBfr']).text
                discount = self.driver.find_element_by_xpath(xpaths['discount']).text
            except:
                priceBfr = priceNow
                discount = '0'
            colorsBtn = self.driver.find_elements_by_xpath(xpaths['colorsBtn'])
            colors, allSizes, allImages = [], [], []
            for c in range(len(colorsBtn)):
                colorsBtn = self.driver.find_elements_by_xpath(xpaths['colorsBtn'])
                if c < len(colorsBtn): # Founds 2x then 1x
                    c = colorsBtn[c]
                    sleep(1)
                    try:
                        c.click()
                    except:
                        sleep(2)
                        c.click()
                    colors.append(c.get_attribute('src'))
                    sizes, images = [], []
                    sizesTags = self.driver.find_elements_by_xpath(xpaths['sizesTags'])
                    for s in sizesTags:
                        try:
                            s.find_element_by_xpath(xpaths['coming'])
                            sizes.append(f'{s.get_attribute("innerText")}(Próximamente)')
                        except:
                            if "is-disabled" in s.get_attribute("class"):
                                sizes.append(f'{s.get_attribute("innerText")}(AGOTADO)')
                            else:
                                sizes.append(s.get_attribute('innerText'))
                    if not sizes:
                        sizes = ['Única']
                    allSizes.append(sizes)
                    self.driver.find_element_by_xpath('.//body').send_keys(Keys.END)
                    while not images:
                        sleep(1)
                        for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                            images.append(i.get_attribute('src'))
                    allImages.append(images)
                    self.driver.find_element_by_xpath('.//body').send_keys(Keys.HOME)
            if not colorsBtn:
                sizes, images = [], []
                sizesTags = self.driver.find_elements_by_xpath(xpaths['sizesTags'])
                for s in sizesTags:
                    try:
                        s.find_element_by_xpath(xpaths['coming'])
                        sizes.append(
                            f'{s.get_attribute("innerText")}(Próximamente)'
                        )
                    except:
                        if 'is-disabled' in s.get_attribute('class'):
                            sizes.append(
                                f'{s.get_attribute("innerText")}(AGOTADO)'
                            )
                        else:
                            sizes.append(s.get_attribute('innerText'))
                if not sizes:
                    sizes = ['Única']
                allSizes.append(sizes)
                self.driver.find_element_by_xpath('.//body').send_keys(Keys.END)
                if len(self.driver.find_elements_by_xpath(xpaths['imgs'])) < 2:
                    sleep(3)
                for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                    images.append(i.get_attribute('src')) # .replace('/2021/I/','/2021/V/'))
                allImages.append(images)
                colors.append(images[0])
            db.add(Item(brand, name, ref, description, priceBfr, priceNow, discount, allImages, url, allSizes, colors, self.category, self.originalCategory, self.subcategory, self.originalSubcategory, self.gender))
        except Exception as e:
            print('Item saltado', url)
            print(e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


def scrap_for_links():
    driver = webdriver.Chrome('./chromedriver')
    driver.set_page_load_timeout(40)
    driver.maximize_window()
    driver.get('https://www.bershka.com/co/')
    try:
        driver.find_element_by_xpath('.//button[@class="modal__close-button"]').click()
        sleep(2)
        driver.find_element_by_xpath('.//button[@class="modal__close-button"]').click()
    except:
        pass
    main_categories = []
    for c in driver.find_elements_by_xpath(xpaths['categories']):
        url = c.get_attribute('href')
        if '/mujer/' in url:
            main_categories.append(url)
    get_network = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;'
    endpoints.clear()
    news = ''
    for c in main_categories:
        driver.get(c)
        m = 0
        for i in range(10):
            net = driver.execute_script(get_network)
            if len(net) > m:
                net_data = net
                m = len(net)
            sleep(.3)
        for i in net_data:
            if '/product?' in i['name']:
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
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://www.bershka.com/',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'][randint(0, 4)]}
        session.headers.update(headers)
        image_formats = ('image/png', 'image/jpeg', 'image/jpg')
        filename = './Files/LogsBERSHKA.txt'
        with open(filename, 'w') as logs:
            logs.write(f'··········{datetime.now(tz).month} - {datetime.now(tz).day}··········\n')
        for endpoint in endpoints:
            products = session.get(endpoint[1]).json()['products']
            logs = open(filename, 'a')
            logs.write(f'{datetime.now(tz).hour}:{datetime.now(tz).minute}   -   {len(products)} productos  -  {endpoint[0]}\n')
            logs.close()
            for product in products:
                logs = open(filename, 'a')
                try:
                    name = product['name']
                    prod_id = product['id']
                    category = product['relatedCategories'][0]['name']
                    product = product['bundleProductSummaries'][0]['detail']
                    description = product['description'] if product['description'] else product['longDescription']
                    ref = product['displayReference']
                    subcategory = product['subfamilyInfo']['subFamilyName']
                    url = f'https://www.bershka.com/co/{name.lower().replace(" ","-")}-c0p{prod_id}.html'
                    colors, all_images, all_sizes = [], [], []
                    for color in product['colors']:
                        colors.append(f'https://static.bershka.net/4/photos2{color["image"]["url"]}_2_4_5.jpg?t={color["image"]["timestamp"]}')
                        sizes = []
                        for size in color['sizes']:
                            stock = '' if size['visibilityValue'] == 'SHOW' else '(AGOTADO)'
                            sizes.append(size['name'] + stock)
                        all_sizes.append(sizes)
                    # if not all([all(['(AGOTADO)' in size for size in sizes]) for sizes in all_sizes]):
                    price_now = [int(product['colors'][0]['sizes'][0]['price']) / 100]
                    try:
                        price_before = int(product['colors'][0]['sizes'][0]['oldPrice']) / 100
                    except TypeError:
                        price_before = price_now[0]

                    item = Item(brand,name,ref,description,price_before,price_now,0,all_images,url,all_sizes,colors,category,category,subcategory,subcategory,'Mujer')
                    optional_images = []
                    for media in product['xmedia']:
                        color = []
                        for i in media['xmediaItems'][0]['medias']:
                            if not '_2_6_' in i['idMedia']:
                                color.append(f'https://static.bershka.net/4/photos2/{media["path"]}/{i["idMedia"]}3.jpg?ts={i["timestamp"]}')
                        optional_images.append(color)
                    image = ''
                    for color in optional_images:
                        for i in color:
                            if not image:
                                r = session.head(i)
                                if r.headers["content-type"] in image_formats:
                                    image = i
                                else:
                                    color.remove(i)
                    found = db.contains(url, image,sync=True)
                    if found:
                        item.allImages = found['allImages']
                    else:
                        for color in optional_images:
                            images = []
                            for image in color:
                                if len(optional_images) == 1 or len(images) < 2:
                                    r = session.head(image)
                                    if r.headers["content-type"] in image_formats:
                                        images.append(image)
                            all_images.append(images)
                        item.allImages = all_images
                    db.add(item)
                    logs.write(f'    + {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {name}\n')
                    # else:
                    #     logs.write(f'X {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {name} SIN STOCK\n')
                except Exception as e:
                    print(e)
                    logs.write(f'X {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {e}\n')
                logs.close()
            headers = session.headers
            sleep(randint(30, 120))
            session = requests.session()
            session.headers.update(headers)

# Main Code
# ScrapBershka()
