import ast
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Item import Item
from Database import Database

BRAND = 'Mercedes Campuzano'
XPATHS = {
    'categories': './/ul[@class="vtex-menu-2-x-menuContainer list flex pl0 mv0 flex-row"]/div/div/div/div/div/li/div',
    'close_btn': './/button[@class="vtex-modal-layout-0-x-closeButton vtex-modal-layout-0-x-closeButton--modal-header ma0 bg-transparent pointer bw0 pa3"]',
    'color': './/img[@class="vtex-store-components-3-x-skuSelectorItemImageValue mercedescampuzano-mcampuzano-1-x-showImgColor"]',
    'colors_btn': './/ul[@class="vtex-slider-0-x-sliderFrame list pa0 h-100 ma0 flex justify-center"]/li[not(.//button)]',
    'description': './/div[@class="vtex-store-components-3-x-specificationsTableContainer mt9 mt0-l pl8-l"]',
    'description2': './/div[@class="vtex-store-components-3-x-content vtex-store-components-3-x-content--product-description h-auto"]',
    'discount': './/div[@class="vtex-store-components-3-x-discountInsideContainer t-mini white absolute right-0 pv2 ph3 bg-emphasis z-1"]',
    'elems': './/section[@class="vtex-product-summary-2-x-container vtex-product-summary-2-x-containerNormal overflow-hidden br3 h-100 w-100 flex flex-column justify-between center tc"]',
    'href': "./a",
    'fast_discount': './a//div[contains(@class,"discountInsideContainer")]',
    'fast_priceBfr': './a//div/span[contains(@class,"strike")]/span',
    'fast_priceNow': './a//div/span[@class="vtex-store-components-3-x-sellingPrice vtex-store-components-3-x-sellingPriceValue vtex-product-summary-2-x-sellingPrice vtex-product-summary-2-x-sellingPrice--sosPrice dib ph2 t-body t-heading-5-ns vtex-product-summary-2-x-price_sellingPrice vtex-product-summary-2-x-price_sellingPrice--sosPrice"]/span',
    'imgs': './/div[contains(@class,"swiper-slide vtex-store-components-3-x-productImagesGallerySlide center-all")]/div/div/div/img',
    'name': './/span[@class="vtex-store-components-3-x-productBrand "]',
    'name2': './/span[contains(@class,"vtex-store-components-3-x-currencyInteger vtex-store-components-3-x-currencyInteger--price"]',
    'priceBfr': './/div[contains(@class,"priceContainer")]/div/span',
    'priceNow': './/span[contains(@class,"vtex-store-components-3-x-price_sellingPrice--price")]',
    'prices': './/span[@class="vtex-store-components-3-x-currencyContainer vtex-store-components-3-x-currencyContainer--price"]',
    'ref': '',
    'sale_category': './/a[@class="vtex-breadcrumb-1-x-link vtex-breadcrumb-1-x-link--1 dib pv1 link ph2 c-muted-2 hover-c-link"]',
    'subcategories': './/div[contains(@class,"vtex-menu-2-x-submenuContainer ")]/div/section/nav/ul/li/div/a',
    'subcategories2': './/a[@class="vtex-slider-layout-0-x-imageElementLink vtex-slider-layout-0-x-imageElementLink--menu-slider vtex-store-components-3-x-imageElementLink vtex-store-components-3-x-imageElementLink--menu-slider"]',
}
db = Database(BRAND)
try:
    endpoints = ast.literal_eval(open('./Files/Settings.json','r').read())[BRAND]['endpoints']
except:
    endpoints = []

class ScrapMercedesCampuzano:
    def __init__(self):
        self.opts = webdriver.ChromeOptions()
        self.opts.headless = True
        self.opts.add_argument('--window-size=1920,1080')
        self.opts.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.opts)
        self.driver.set_page_load_timeout(30)
        # self.driver = webdriver.Chrome('./chromedriver')
        # self.driver.maximize_window()
        self.gender = 'Mujer'
        self.sale = False
        mouse = webdriver.ActionChains(self.driver)
        self.driver.get('https://www.mercedescampuzano.com/')
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, XPATHS['close_btn']))).click()
        categories = self.driver.find_elements_by_xpath(XPATHS['categories'])
        subcategories = []
        for c in categories:
            mouse.move_to_element(c).perform()
            for s in self.driver.find_elements_by_xpath(XPATHS['subcategories']):
                try:
                    subcategories.append((s.text, s.get_attribute('href')))
                except:
                    pass
            if not self.driver.find_elements_by_xpath(XPATHS['subcategories']):
                for s in self.driver.find_elements_by_xpath(
                        XPATHS['subcategories2']):
                    subcategories.append(s.get_attribute('href'))
        for c in subcategories:
            self.category = c[0]
            self.subcategory = self.category
            self.originalCategory = self.category
            self.originalSubcategory = self.category
            self.scrapCategory(c[1])
        self.driver.quit()

    def scrapCategory(self, url):
        self.driver.get(url)
        sleep(5)
        if self.sale:
            self.category = self.driver.find_element_by_xpath(XPATHS['sale_category']).text
            self.subcategory = self.category
            self.originalCategory = self.category
            self.originalSubcategory = self.category
        loading = True
        elems = self.driver.find_elements_by_xpath(XPATHS['elems'])
        while loading:
            try:
                self.driver.find_element_by_xpath('.//body').send_keys(
                    Keys.END)
                sleep(3)
                self.driver.find_element_by_xpath('.//body').send_keys(
                    Keys.PAGE_UP)
                sleep(1)
                self.driver.find_element_by_xpath('.//body').send_keys(
                    Keys.PAGE_UP)
                sleep(2)
                if len(elems) == len(
                        self.driver.find_elements_by_xpath(XPATHS['elems'])):
                    sleep(3)
                loading = len(elems) < len(
                    self.driver.find_elements_by_xpath(XPATHS['elems']))
                elems = self.driver.find_elements_by_xpath(XPATHS['elems'])
            except:
                loading = False
        for elem in elems:
            self.driver.execute_script('arguments[0].scrollIntoView();', elem)
            url = elem.find_element_by_xpath(
                XPATHS['href']).get_attribute('href')
            if db.contains(url):
                db.update_product(elem, url, XPATHS)
            else:
                self.scrapProduct(url)

    def scrapProduct(self, url):
        try:
            self.driver.execute_script(
                'window.open("{}", "new window")'.format(url))
            self.driver.switch_to.window(self.driver.window_handles[1])
            try:
                priceNow = self.driver.find_elements_by_xpath(
                    XPATHS['prices'])[1].text  # 16/03/21
                priceBfr = self.driver.find_elements_by_xpath(
                    XPATHS['prices'])[0].text
                discount = self.driver.find_element_by_xpath(
                    XPATHS['discount']).text
            except:
                try:
                    priceNow = self.driver.find_elements_by_xpath(
                        XPATHS['prices'])[0].text  # 16/03/21
                except:
                    try:
                        priceNow = self.driver.find_element_by_xpath(
                            XPATHS['priceNow']).text
                    except:
                        sleep(3)
                        priceNow = self.driver.find_element_by_xpath(
                            XPATHS['priceNow']).text
                priceBfr = priceNow
                discount = ' '
            ref = 'ref'
            try:
                description = self.driver.find_element_by_xpath(
                    XPATHS['description']).get_attribute('innerText')
            except:
                description = self.driver.find_element_by_xpath(
                    XPATHS['description2']).get_attribute('innerText')
            colors_btn = self.driver.find_elements_by_xpath(XPATHS['colors_btn'])
            colors = []
            allSizes = []
            comunName = []
            skipName = [[], []]
            allImages = []
            # self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_DOWN)
            for c in range(len(colors_btn) + 1):
                try:
                    name = self.driver.find_element_by_xpath(
                        XPATHS['name']).text
                except:
                    name = self.driver.find_element_by_xpath(
                        XPATHS['name2']).text
                if not comunName:
                    comunName = name.split(' ')
                else:
                    for j in comunName:
                        if not j in name:
                            comunName.remove(j)
                w = name.split(' ')[0]
                if w in skipName[0]:
                    skipName[1][skipName[0].index(w)] = (
                        skipName[1][skipName[0].index(w)] + 1)
                else:
                    skipName[0].append(w)
                    skipName[1].append(1)
                colors_btn = self.driver.find_elements_by_xpath(
                    XPATHS['colors_btn'])
                colors_btn.insert(0, 'init')
                if c > 0:
                    colors_btn[c].click()
                try:
                    colors.append(
                        self.driver.find_element_by_xpath(
                            XPATHS['color']).get_attribute('src'))
                except:
                    sleep(3)
                    try:
                        colors.append(
                            self.driver.find_element_by_xpath(
                                XPATHS['color']).get_attribute('src'))
                    except:
                        sleep(2)
                        try:
                            colors.append(
                                self.driver.find_element_by_xpath(
                                    XPATHS['color']).get_attribute('src'))
                        except:
                            colors.append(
                                self.driver.find_element_by_xpath(
                                    XPATHS['imgs']).get_attribute('src'))
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath(
                    './/div[contains(@class,"flex flex-column vtex-store-components-3-x-skuSelectorSubcontainer--talla mb3 vtex-store-components-3-x-skuSelectorSubcontainer")]/div/div[@class="vtex-store-components-3-x-skuSelectorOptionsList w-100 inline-flex flex-wrap ml2 items-center"]/div'
                )
                for s in sizesTags:
                    if s.find_elements_by_xpath(
                            './div/div[@class="absolute absolute--fill vtex-store-components-3-x-diagonalCross"]'
                    ):
                        sizes.append('{}(AGOTADO)'.format(
                            s.get_attribute('innerText')))
                    else:
                        sizes.append(s.get_attribute('innerText'))
                if not sizes:
                    sizes = ['Única']
                allSizes.append(sizes)
                images = []
                imgs = self.driver.find_elements_by_xpath(XPATHS['imgs'])
                while not imgs:
                    sleep(1)
                    imgs = self.driver.find_elements_by_xpath(XPATHS['imgs'])
                for i in imgs:
                    images.append(i.get_attribute('src'))
                allImages.append(images)
            name = ' '.join(comunName)
            w = skipName[0][skipName[1].index(max(skipName[1]))]
            if not name.startswith(w):
                name = ' '.join([w, name])
            db.add(Item(BRAND, name, ref, description, priceBfr, priceNow, discount, allImages, url, allSizes, colors, self.category, self.originalCategory, self.subcategory, self.originalSubcategory, self.gender))
        except Exception as e:
            print('Item saltado', url)
            print(e)
            # inst = input('Continuar...')
            # while inst != '':
            #    try:
            #        exec(print(inst))
            #    except:
            #        print('err')
            #    inst = input('...')
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


def scrap_for_links():
    opts = webdriver.ChromeOptions()
    # opts.headless = True
    opts.add_argument('--window-size=1920,1080')
    opts.add_argument('--start-maximized')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    driver.set_page_load_timeout(30)
    driver.get('https://www.mercedescampuzano.com/')
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, XPATHS['close_btn']))).click()
    mouse = webdriver.ActionChains(driver)
    categories = driver.find_elements_by_xpath(XPATHS['categories'])
    subcategories = []
    for c in categories:
        mouse.move_to_element(c).perform()
        for s in driver.find_elements_by_xpath(XPATHS['subcategories']):
            try:
                subcategories.append(s.get_attribute('href'))
            except:
                pass
    look_network = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;'
    new = ''
    for c in subcategories:
        driver.get(c)
        endpoint = ''
        count = 0
        while not endpoint and count < 10:
            count += 1
            netData = driver.execute_script(look_network)
            for i in netData:
                if 'recommendation/popular' in i['name']:
                    endpoint = i['name']
                    if not endpoint in str(endpoints):
                        endpoints.append([c, endpoint])
                        print(endpoint)
                        if 'destacados/nuevo' in c:
                            new = endpoint
            if not endpoint:
                sleep(1)
        input('...')
    driver.quit()
    settings = ast.literal_eval(open('./Files/Settings.json','r').read())
    settings[BRAND]['endpoints'] = endpoints
    settings[BRAND]['endpoint'] = new if new else endpoints[0][1]
    with open('./Files/Settings.json','w') as s:
        s.write(str(settings).replace("'",'"'))


class APICrawler:
    def __init__(self, endpoints=endpoints):
        ScrapMercedesCampuzano()

# Main Code
# ScrapMercedesCampuzano()
