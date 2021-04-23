from Item import Item
from time import sleep
from Database import Database
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

xpaths={
    'categories' : './/ul[@class="vtex-menu-2-x-menuContainer list flex pl0 mv0 flex-row"]/div/div/div/div/div/li/div/a',
    'closeBtn' : './/button[@class="vtex-modal-layout-0-x-closeButton vtex-modal-layout-0-x-closeButton--modal-header ma0 bg-transparent pointer bw0 pa3"]',
    'color' : './/img[@class="vtex-store-components-3-x-skuSelectorItemImageValue mercedescampuzano-mcampuzano-1-x-showImgColor"]',
    'colorsBtn' : './/ul[@class="vtex-slider-0-x-sliderFrame list pa0 h-100 ma0 flex justify-center"]/li[not(.//button)]',
    'description' : './/div[@class="vtex-store-components-3-x-specificationsTableContainer mt9 mt0-l pl8-l"]',
    'description2' : './/div[@class="vtex-store-components-3-x-content vtex-store-components-3-x-content--product-description h-auto"]',
    'discount' : './/div[@class="vtex-store-components-3-x-discountInsideContainer t-mini white absolute right-0 pv2 ph3 bg-emphasis z-1"]',
    #'elems' : './/div[@class="vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--gallery vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--gallery--normal vtex-search-result-3-x-galleryItem--grid vtex-search-result-3-x-galleryItem--gallery--grid pa4"]',
    'elems' : './/a[@class="vtex-product-summary-2-x-clearLink h-100 flex flex-column"]/@href',
    'imgs' : './/div[contains(@class,"swiper-slide vtex-store-components-3-x-productImagesGallerySlide center-all")]/div/div/div/img',
    'name' : './/span[@class="vtex-store-components-3-x-productBrand "]',
    'name2' : './/span[contains(@class,"vtex-store-components-3-x-currencyInteger vtex-store-components-3-x-currencyInteger--price"]',
    'priceNow' : './/span[@class="vtex-product-price-1-x-currencyContainer vtex-product-price-1-x-currencyContainer--summary"]',
    'prices' : './/span[@class="vtex-store-components-3-x-currencyContainer vtex-store-components-3-x-currencyContainer--price"]',
    'saleCategory' : './/a[@class="vtex-breadcrumb-1-x-link vtex-breadcrumb-1-x-link--1 dib pv1 link ph2 c-muted-2 hover-c-link"]'
}

class ScrapMercedesCampuzano:
    def __init__(self):
        """options = Options()
        options.add_argument("enable-automation")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome("./chromedriver.exe",options=options)"""
        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.driver.set_page_load_timeout(30)
        self.brand = "Mercedes Campuzano"
        self.db = Database(self.brand)
        self.driver.maximize_window()
        self.gender = "Mujer"
        self.driver.get("https://www.mercedescampuzano.com/")
        for i in range(5):
            try:
                self.driver.find_element_by_xpath(xpaths['closeBtn']).click()
                break
            except:
                print('sleep',i)
                sleep(1)
        categories = [self.driver.find_elements_by_xpath(xpaths['categories']),[]]
        for c in categories[0]:
            cat = c.get_attribute("title")
            categories[1].append(c.get_attribute("href"))
            categories[0][categories[0].index(c)] = cat.capitalize()
        for c in categories[0][3:]:
            self.category = c
            self.subcategory = c
            self.originalCategory = c
            self.originalSubcategory = c
            if 'Sale' in categories[0][categories[0].index(c)]:
                self.sale = True
            else:
                self.sale = False
            self.scrapCategory(categories[1][categories[0].index(c)])
        self.driver.close()

    def scrapCategory(self, url):
        self.driver.get(url)
        sleep(5)
        if self.sale:
            self.category = self.driver.find_element_by_xpath(xpaths['saleCategory']).text
            self.subcategory = self.category
            self.originalCategory = self.category
            self.originalSubcategory = self.category
        loading = True
        elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        while loading:
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(3)
                self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_UP)
                sleep(1)
                self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_UP)
                sleep(1)
                loading = len(elems) < len(self.driver.find_elements_by_xpath(xpaths['elems']))
                elems = self.driver.find_elements_by_xpath(xpaths['elems'])
            except:
                loading = False
        for e in elems:
            try:
                self.db.addUrl(e)
                if not self.db.contains(e):
                    self.scrapProduct(e)
            except:
                self.db.urlError(e)

    def scrapProduct(self, url):
        try:
            self.driver.execute_script('window.open("{}", "new window")'.format(url))
            self.driver.switch_to.window(self.driver.window_handles[1])
            try:
                priceNow = self.driver.find_elements_by_xpath(xpaths['prices'])[1].text#16/03/21
                priceBfr = self.driver.find_elements_by_xpath(xpaths['prices'])[0].text
                discount = self.driver.find_element_by_xpath(xpaths['discount']).text
            except:
                try:
                    priceNow = self.driver.find_elements_by_xpath(xpaths['prices'])[0].text#16/03/21
                except:
                    try:
                        priceNow = self.driver.find_element_by_xpath(xpaths['priceNow']).text
                    except:
                        sleep(3)
                        priceNow = self.driver.find_element_by_xpath(xpaths['priceNow']).text
                priceBfr = priceNow
                discount = ' '
            try:
                description = self.driver.find_element_by_xpath(xpaths['description']).get_attribute('innerText')
            except:
                description = self.driver.find_element_by_xpath(xpaths['description2']).get_attribute('innerText')
            colorsBtn = self.driver.find_elements_by_xpath(xpaths['colorsBtn'])
            colors = []
            allSizes = []
            comunName = []
            skipName=[[],[]]
            allImages = []
            #self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_DOWN)
            for c in range(len(colorsBtn)+1):
                try:
                    name = self.driver.find_element_by_xpath(xpaths['name']).text
                except:
                    name = self.driver.find_element_by_xpath(xpaths['name2']).text
                if not comunName:
                    comunName = name.split(" ")
                else:
                    for j in comunName:
                        if not j in name:
                            comunName.remove(j)
                w = name.split(' ')[0]
                if w in skipName[0]:
                    skipName[1][skipName[0].index(w)] = skipName[1][skipName[0].index(w)] + 1
                else:
                    skipName[0].append(w)
                    skipName[1].append(1)
                colorsBtn = self.driver.find_elements_by_xpath(xpaths['colorsBtn'])
                colorsBtn.insert(0,'init')
                if c > 0:
                    colorsBtn[c].click()
                try:
                    colors.append(self.driver.find_element_by_xpath(xpaths['color']).get_attribute("src"))
                except:
                    sleep(3)
                    try:
                        colors.append(self.driver.find_element_by_xpath(xpaths['color']).get_attribute("src"))
                    except:
                        sleep(2)
                        try:
                            colors.append(self.driver.find_element_by_xpath(xpaths['color']).get_attribute("src"))
                        except:
                            colors.append(self.driver.find_element_by_xpath(xpaths['imgs']).get_attribute("src"))
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath('.//div[contains(@class,"flex flex-column vtex-store-components-3-x-skuSelectorSubcontainer--talla mb3 vtex-store-components-3-x-skuSelectorSubcontainer")]/div/div[@class="vtex-store-components-3-x-skuSelectorOptionsList w-100 inline-flex flex-wrap ml2 items-center"]/div')
                for s in sizesTags:
                    if s.find_elements_by_xpath('./div/div[@class="absolute absolute--fill vtex-store-components-3-x-diagonalCross"]'):
                        sizes.append("{}(Agotado)".format(s.get_attribute("innerText")))
                    else:
                        sizes.append(s.get_attribute("innerText"))
                if not sizes:
                    sizes = ["Única"]
                allSizes.append(sizes)
                images = []
                imgs = self.driver.find_elements_by_xpath(xpaths['imgs'])
                while not imgs:
                    sleep(1)
                    imgs = self.driver.find_elements_by_xpath(xpaths['imgs'])
                for i in imgs:
                    images.append(i.get_attribute('src'))
                allImages.append(images)
            name = " ".join(comunName)
            w = skipName[0][skipName[1].index(max(skipName[1]))]
            if not name.startswith(w):
                name = " ".join([w,name])
            Item(self.brand,name,description,priceBfr,priceNow,discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale,self.gender)
        except Exception as e:
            print("Item saltado")
            print(e)
            #inst = input('Continuar...')
            #while inst != '':
            #    try:
            #        exec(print(inst))
            #    except:
            #        print('err')
            #    inst = input('...')
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


# Main Code
#ScrapMercedesCampuzano()