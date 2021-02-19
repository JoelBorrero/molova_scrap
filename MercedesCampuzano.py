import os
from time import sleep
from selenium import webdriver
from Item import Item
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class ScrapMercedes:
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
        self.brand = "Mercedes Campuzano"
        if not os.path.exists("{}/".format(self.brand)):
            os.mkdir("{}/".format(self.brand))
        self.driver.maximize_window()
        self.gender = "Mujer"
        self.driver.get("https://www.mercedescampuzano.com/")
        self.sale = True
        sale = []
        while not self.driver.find_elements_by_xpath('.//div[@class="vtex-slider-layout-0-x-slideChildrenContainer vtex-slider-layout-0-x-slideChildrenContainer--menu-sale flex justify-center items-center w-100"]/a'):
            sleep(1)
        for s in self.driver.find_elements_by_xpath('.//div[@class="vtex-slider-layout-0-x-slideChildrenContainer vtex-slider-layout-0-x-slideChildrenContainer--menu-sale flex justify-center items-center w-100"]/a'):
            sale.append(s.get_attribute('href'))
        for s in sale:
            self.scrapCategory(s)
        self.sale = False
        categories = [self.driver.find_elements_by_xpath('.//section[@class="vtex-menu-2-x-submenu w-100 flex justify-center"]/nav/ul/li/div/a'),[]]
        for c in categories[0]:
            cat = c.get_attribute("title")
            categories[1].append(c.get_attribute("href"))
            categories[0][categories[0].index(c)] = cat
        for c in categories[0]:
            self.category = c
            self.subcategory = c
            self.originalCategory = c
            self.originalSubcategory = c
            self.scrapCategory(categories[1][categories[0].index(c)])

    def scrapCategory(self, url):
        self.driver.get(url)
        sleep(5)
        if self.sale:
            self.category = self.driver.find_element_by_xpath('.//a[@class="vtex-breadcrumb-1-x-link vtex-breadcrumb-1-x-link--1 dib pv1 link ph2 c-muted-2 hover-c-link"]').text
            self.subcategory = self.category
            self.originalCategory = self.category
            self.originalSubcategory = self.category
        loading = False
        elems = self.driver.find_elements_by_xpath('.//a[@class="vtex-product-summary-2-x-clearLink h-100 flex flex-column"]')
        while loading:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            loading = len(elems) < len(self.driver.find_elements_by_xpath('.//a[@class="vtex-product-summary-2-x-clearLink h-100 flex flex-column"]'))
            elems = self.driver.find_elements_by_xpath('.//a[@class="vtex-product-summary-2-x-clearLink h-100 flex flex-column"]')
        for e in elems[:1]:
            self.driver.execute_script("arguments[0].scrollIntoView();", e)
            self.scrapProduct(e.get_attribute("href"))

    def scrapProduct(self, url):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            try:
                name = self.driver.find_element_by_xpath('.//span[@class="vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--quickview "]').text
            except:
                sleep(3)
                name = self.driver.find_element_by_xpath('.//span[@class="vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--quickview "]').text
            print(name)
            try:
                description = self.driver.find_element_by_xpath('.//div[@class="vtex-store-components-3-x-specificationsTableContainer mt9 mt0-l pl8-l"]').get_attribute('innerText')
            except:
                description = self.driver.find_element_by_xpath('.//div[@class="vtex-store-components-3-x-content vtex-store-components-3-x-content--product-description h-auto"]').get_attribute('innerText')
            priceNow = self.driver.find_element_by_xpath('.//span[@class="vtex-product-price-1-x-currencyContainer vtex-product-price-1-x-currencyContainer--summary"]').text
            try:
                priceBfr = self.driver.find_element_by_xpath('.//span[@class="vtex-product-price-1-x-listPrice vtex-product-price-1-x-listPrice--summary"]').text
                discount = self.driver.find_element_by_xpath('.//div[@class="vtex-store-components-3-x-discountInsideContainer t-mini white absolute right-0 pv2 ph3 bg-emphasis z-1"]').text
            except:
                priceBfr = priceNow
                discount = ''
            colorsBtn = self.driver.find_elements_by_xpath('.//ul[@class="vtex-slider-0-x-sliderFrame list pa0 h-100 ma0 flex justify-center"]/li[not(.//button)]')
            colors = []
            allSizes = []
            allImages = []
            #self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_DOWN)
            for c in range(len(colorsBtn)+1):
                colorsBtn = self.driver.find_elements_by_xpath('.//ul[@class="vtex-slider-0-x-sliderFrame list pa0 h-100 ma0 flex justify-center"]/li[not(.//button)]')
                colorsBtn.insert(0,'init')
                if c > 0:
                    colorsBtn[c].click()
                try:
                    colors.append(self.driver.find_element_by_xpath('.//img[@class="vtex-store-components-3-x-skuSelectorItemImageValue mercedescampuzano-mcampuzano-1-x-showImgColor"]').get_attribute("src"))
                except:
                    sleep(3)
                    try:
                        colors.append(self.driver.find_element_by_xpath('.//img[@class="vtex-store-components-3-x-skuSelectorItemImageValue mercedescampuzano-mcampuzano-1-x-showImgColor"]').get_attribute("src"))
                    except:
                        sleep(2)
                        try:
                            colors.append(self.driver.find_element_by_xpath('.//img[@class="vtex-store-components-3-x-skuSelectorItemImageValue mercedescampuzano-mcampuzano-1-x-showImgColor"]').get_attribute("src"))
                        except:
                            print('No color src')
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
                imgs = self.driver.find_elements_by_xpath('.//div[contains(@class,"swiper-slide vtex-store-components-3-x-productImagesGallerySlide center-all")]/div/div/div/img')
                while not imgs:
                    sleep(1)
                    imgs = self.driver.find_elements_by_xpath('.//div[contains(@class,"swiper-slide vtex-store-components-3-x-productImagesGallerySlide center-all")]/div/div/div/img"]')
                for i in imgs:
                    images.append(i.get_attribute('src'))
                allImages.append(images)
            Item(self.brand,name,description,priceBfr,priceNow,discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale,self.gender)
        except Exception as e:
            i = 0
            if not os.path.exists("{}/Errors/".format(self.brand)):
                os.mkdir("{}/Errors/".format(self.brand))
            while os.path.exists('{}/Errors/{}{}.png'.format(self.brand, e, i)):
                i = i + 1
            self.driver.save_screenshot('{}/Errors/{}{}.png'.format(self.brand, e, i))
            print("Item saltado")
            print(e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


# Main Code
ScrapMercedes()