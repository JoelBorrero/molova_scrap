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
    'colorsBtn': './/ul[@class="swiper-wrapper"]/li/a/div/img',
    'coming': './span/span/span',
    'description': './/section[@class="product-info"]',
    'discount': './/span[@class="discount-tag"]',
    'elems': './/ul[@class="grid-container"]/li/div/a',
    'fast_discount': './div/div/span',
    'fast_priceBfr':'.//span[@class="old-price-elem"]',
    'fast_priceNow':'.//div[contains(@class,"current-price-elem")]',
    'imgs': './/div/button/div[@class="image-item-wrapper"]/img',
    'name': './/h1[@class="product-title"]',
    'priceBfr': './/span[@class="old-price-elem"]|.//div[@class="top-group"]/div/div[@class="current-price-elem"]',
    'priceNow': './/div[contains(@class,"current-price-elem")]',
    'ref': './/div[@class="product-reference"]',
    'sale': './/ul[@class="sub-menu-container is-active"]/li/a',
    'sizesTags': './/div[@class="sizes-list-detail"]/ul/li/button',
    'subCats': './/div[@class="filter-tag-swiper"]/div/ul/li',
}
try:
    endpoints = ast.literal_eval(open('./.settings','r').read())[brand]['endpoints']
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
            cat = c.get_attribute('innerText').replace('\n', '')
            categories[1].append(c.get_attribute('href'))
            while cat.startswith(' '):
                cat = cat[1:]
            while cat.endswith(' '):
                cat = cat[:-1]
            categories[0].append(cat)
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
                    # try:
                    self.driver.find_element_by_xpath('.//body').send_keys(Keys.HOME)
                    sleep(1)
                    subCats[s].click()
                    self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_DOWN)
                    sleep(1)
                    subCats = self.driver.find_elements_by_xpath(xpaths['subCats'])
                    self.subcategory = subCats[s].get_attribute('innerText')
                    self.originalSubcategory = subCats[s].get_attribute('innerText')
                    self.scrapSubcategory()
                    # except:
                    #     print('Error clicking')
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
            colors = []
            allSizes = []
            allImages = []
            for c in colorsBtn:
                try:
                    c.click()
                except:
                    sleep(2)
                    c.click()
                colors.append(c.get_attribute('src'))
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath(xpaths['sizesTags'])
                for s in sizesTags:
                    try:
                        s.find_element_by_xpath(xpaths['coming'])
                        sizes.append(f'{s.get_attribute("innerText")}(Próximamente)')
                    except:
                        if "is-disabled" in s.get_attribute("class"):
                            sizes.append(f'{s.get_attribute("innerText")}(Agotado)')
                        else:
                            sizes.append(s.get_attribute('innerText'))
                if not sizes:
                    sizes = ['Única']
                allSizes.append(sizes)
                images = []
                self.driver.find_element_by_xpath('.//body').send_keys(Keys.END)
                while not images:
                    sleep(1)
                    for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                        images.append(i.get_attribute('src'))
                allImages.append(images)
                self.driver.find_element_by_xpath('.//body').send_keys(Keys.HOME)
            if not colorsBtn:
                sizes = []
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
                                f'{s.get_attribute("innerText")}(Agotado)'
                            )
                        else:
                            sizes.append(s.get_attribute('innerText'))
                if not sizes:
                    sizes = ['Única']
                allSizes.append(sizes)
                images = []
                self.driver.find_element_by_xpath('.//body').send_keys(Keys.END)
                if len(self.driver.find_elements_by_xpath(xpaths['imgs'])) < 2:
                    sleep(3)
                for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                    images.append(i.get_attribute('src').replace('/2021/I/','/2021/V/'))
                allImages.append(images)
                colors.append(images[0])
            db.add(
                Item(
                    brand,
                    name,
                    ref,
                    description,
                    priceBfr,
                    priceNow,
                    discount,
                    allImages,
                    url,
                    allSizes,
                    colors,
                    self.category,
                    self.originalCategory,
                    self.subcategory,
                    self.originalSubcategory,
                    self.sale,
                    self.gender,
                )
            )
        except Exception as e:
            print('Item saltado', url)
            print(e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


def scrap_for_links():
    driver = webdriver.Chrome('./chromedriver')
    driver.set_page_load_timeout(30)
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
        main_categories.append(c.get_attribute('href'))
    get_network = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;'
    endpoints.clear()
    news = ''
    for c in main_categories:
        driver.get(c)
        sleep(1)
        netData = driver.execute_script(get_network)
        for i in netData:
            if 'products?ajax' in i['name']:
                endpoints.append((c,i['name']))
                if 'nuevo-' in c:
                    news = i['name']
    driver.quit()
    settings = ast.literal_eval(open('./.settings','r').read())
    settings[brand]['endpoints'] = endpoints
    settings[brand]['endpoint'] = news if news else endpoints[0][1]
    with open('./.settings','w') as s:
        s.write(str(settings))


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
        filename = './Database/LogsBERSHKA.txt'
        open(filename, 'w').close()
        for endpoint in endpoints:
            logs = open(filename, 'a')
            products = session.get(endpoint[1]).json()['products']
            logs.write(f'{datetime.now(tz).hour}:{datetime.now(tz).minute}   -   {len(products)} productos  -  {endpoint[0]}\n')
            logs.close()
            for product in products:
                try:
                    name = product['name']
                    
                except Exception as e:
                    logs = open(filename, 'a')
                    logs.write(f'X {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {e}\n')
                    logs.close()
                    print(e)
            headers = session.headers
            sleep(randint(120,300))
            session = requests.session()
            session.headers.update(headers)

# Main Code
# ScrapBershka()
