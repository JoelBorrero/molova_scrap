import ast
import requests
from time import sleep
from random import uniform
from datetime import datetime
import pytz
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Item import Item
from Database import Database

brand = 'Stradivarius'
db = Database(brand)
tz = pytz.timezone('America/Bogota')
xpaths = {
    'categories': './/div[@class="categories-menu "]/div[contains(@class,"items-menu")]/div/a[not(@href="javascript:void(0)")]|.//div[@class="categories-menu "]/div[contains(@class,"items-menu")]/div[./a[@href="javascript:void(0)"]]/following-sibling::div[position()=1]//a',
    'categoriesSale': './/ul[@class="product-categories"]/li/ul/li/a[span[contains(@style,"#f")]]',
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
    'priceBfr':'.//div[@class="product-price block-height"]//div[@class="one-old-price"]//span|.//div[@class="product-price block-height"]//div[@class="current-price"]//span',
    'priceNow':'.//div[@class="product-price block-height"]//div[@class="current-price"]//span',
    'priceNow2':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div/span',
    'ref': './/div[@class="product-ref-details block-height "]/span',
    'sizesTags':'.//div[@id="productComponentRight"]//div[@class="size-grid-sizes-container"]//span',
    'subCats':'.//div[@class="display-inline-block child-center-parent slider-items-container"]/div/a',
    'subCats2':'.//div[@class="category-badges-list"]/a[not(text()="Ver todo")]'}
try:
    endpoints = ast.literal_eval(open('./Files/Settings.json','r').read())[brand]['endpoints']
except:
    endpoints = []


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
            all_sizes = []
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
                all_sizes.append(sizes)
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
                    all_sizes.append(["Única"])
            if name and allImages:
                name = name[0].text.capitalize()
                if not self.originalSubcategory:
                    self.originalSubcategory = ' '
                item = Item(brand,name,ref,description,priceBfr,priceNow,discount,allImages,url,all_sizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,"Mujer")
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
    news = ''
    for c in main_categories:
        if not 'javascript:void' in c:
            driver.get(c)
            sleep(1)
            netData = driver.execute_script(get_network)
            for i in netData:
                if all(e in i['name'] for e in ['https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/','product?']) and i['name'] not in endpoints:
                    endpoints.append([c,i['name']])
                    if 'nuevo-c' in c:
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
        filename = './Files/LogsSTR.txt'
        with open(filename, 'w') as logs:
            logs.write(f'··········{datetime.now(tz).month} - {datetime.now(tz).day}··········\n')
        for endpoint in endpoints:
            res = session.get(endpoint[1]).json()
            logs = open(filename, 'a')
            logs.write(f'{datetime.now(tz).hour}:{datetime.now(tz).minute}   -   {len(res["products"])} productos  -  {endpoint[0]}\n')
            logs.close()
            for product in res['products']:
                logs = open(filename, 'a')
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
                    except:
                        price_bfr = price_now
                    url = f'{endpoint[0][:endpoint[0].index("-c")]}/{quote(name.lower().replace(" ","-"))}-c{cat_id}p{prod_id}.html'
                    all_sizes = []
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
                        all_sizes.append(sizes)
                    if not all([all(['(AGOTADO)' in size for size in sizes]) for sizes in all_sizes]):
                        allImages = []
                        item = Item(brand,name,ref,description,price_bfr,[price_now],0,allImages,url,all_sizes,colors,category,category,subcategory,subcategory,'Mujer')
                        optional_images = []
                        for media in product['xmedia']:
                            color = []
                            for i in media['xmediaItems'][0]['medias']:
                                color.append(f'https://static.e-stradivarius.net/5/photos3{media["path"]}/{i["idMedia"]}2.jpg?t={i["timestamp"]}')
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
                                allImages.append(images)
                            item.allImages = allImages
                        db.add(item)
                        logs.write(f'    + {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {name}\n')
                    else:
                        logs.write(f'X {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {name} SIN STOCK\n')
                except Exception as e:
                    logs.write(f'X {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {e}\n')
                    print(e)
                logs.close()
            headers = session.headers
            sleep(uniform(30, 120))
            session = requests.session()
            session.headers.update(headers)


# Main Code
# ScrapStradivarius()
# mouse = webdriver.ActionChains(self.driver)
# mouse.move_to_element(self.driver.find_element_by_xpath('.//div[@class="child-center-parent sidebar-close col-xs-2"]')).click()
