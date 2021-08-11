import os
from Item import Item
from time import sleep
from Database import Database
from selenium import webdriver

brand = "Zara"
db = Database(brand)
xpaths = {
    'categories': './/ul[@class="layout-categories__container"]/li[position()=1]/ul/li/ul/li/a',
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
    'priceBfr': './/div[@class="product-detail-info__price-amount price"]//span[@class="price__amount price__amount--old"]',
    'priceNow': './/div[@class="product-detail-info__price-amount price"]//span[@class="price__amount-current-wrapper"]',
    'sale': '',
    'sizesTags': './/div[@class="product-detail-info product-detail-view__product-info"]//ul[@class="product-detail-size-selector__size-list"]/li',
    'subcategory': './/span[@class="category-topbar-related-categories__category-name category-topbar-related-categories__category-name--selected"]',
    'subCats':'.//li[@class="variable-width-carousel__item"]/a/div/span',
    'thumbnails': './/ul[@class="product-detail-images-thumbnails product-detail-images__thumbnails"]/li/button',
}

class ScrapZara:
    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")
        self.driver.set_page_load_timeout(30)
        self.sale = False
        self.driver.maximize_window()
        self.driver.get("https://www.zara.com/co/")
        sleep(3)
        try:
            self.driver.find_element_by_xpath('.//button[@class="modal__close-button"]').click()
            print('clicked')
            sleep(2)
            self.driver.find_element_by_xpath('.//button[@class="modal__close-button"]').click()
        except:
            print('No dismiss')
        cats=[[],[]]
        for cat in self.driver.find_elements_by_xpath(xpaths['categories']):
            c = cat.get_attribute('innerText').capitalize()
            cats[0].append(c)
            cats[1].append(cat.get_attribute("href"))
        cats[0].reverse()
        cats[1].reverse()
        for i in range(17, len(cats[0])):
            self.category = cats[0][i]
            self.originalCategory = self.category
            if 'mujer' in cats[1][i] or 'woman' in cats[1][i]:
                self.gender = 'Mujer'
                self.scrapCategoria(cats[1][i])
            else:
                self.gender = 'Hombre'
            # self.scrapCategoria(cats[1][i])

    def scrapCategoria(self, url):
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
                        self.scrapSubcategory()
                    except:
                        # try:
                        self.driver.find_element_by_xpath('.//button[@class="variable-width-carousel__arrow variable-width-carousel__arrow--right"]').click()
                        sleep(1)
                        subcats[s].click()
                        sleep(5)
                        self.subcategory = self.driver.find_element_by_xpath(xpaths['subcategory']).text.capitalize()
                        self.scrapSubcategory()
                        # except:
                        #     print('Never click')
                subcats = self.driver.find_elements_by_xpath(xpaths['subCats'])
        else:
            self.scrapSubcategory()
            
    def scrapSubcategory(self):
        self.originalSubcategory = self.subcategory
        itemsWebElems = self.driver.find_elements_by_xpath(xpaths['elems'])
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        loading = True
        while loading:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            loading = len(itemsWebElems) < len(self.driver.find_elements_by_xpath(xpaths['elems']))
            itemsWebElems = self.driver.find_elements_by_xpath(xpaths['elems'])
        while itemsWebElems:
            elem = itemsWebElems.pop()
            self.driver.execute_script("arguments[0].scrollIntoView();", elem)
            url = elem.find_element_by_xpath(xpaths['href']).get_attribute('href')
            try:
                image = elem.find_element_by_xpath(xpaths['fast_image']).get_attribute('src')
                if db.contains(url, image):
                    db.update_product(elem, url, xpaths)
                else:
                    self.scrapProduct(url)
            except:
                self.scrapProduct(url)


    def scrapProduct(self, url):
        mouse = webdriver.ActionChains(self.driver)
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            name = self.driver.find_element_by_xpath(xpaths['name']).text.capitalize()
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
                colors.append(color.text.replace("Color: ", "").replace('"', "").capitalize())
                sizes = []
                for t in self.driver.find_elements_by_xpath(xpaths['sizesTags']):
                    if "disabled" in t.get_attribute("class"):
                        sizes.append("{}(Agotado)".format(t.find_element_by_xpath("./div/div/span").get_attribute("innerText")))
                    else:
                        sizes.append(t.find_element_by_xpath("./div/div/span").get_attribute("innerText"))
                allSizes.append(sizes)
                images = []
                thumbnails = self.driver.find_elements_by_xpath(xpaths['thumbnails'])
                for i in range(len(thumbnails)):
                    mouse.move_to_element(thumbnails[i]).perform()
                    thumbnails[i].click()
                for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                    if not 'transparent-background' in i.get_attribute("src"):
                        images.append(i.get_attribute("src"))
                allImages.append(images)
            for c in range(len(colorsBtn)):
                colorsBtn[c].click()
                sizes = []
                while not self.driver.find_elements_by_xpath('.//ul[contains(@id,"product-size-selector-product-detail-info")]/li'):
                    sleep(0.1)
                for t in self.driver.find_elements_by_xpath('.//ul[contains(@id,"product-size-selector-product-detail-info")]/li'):
                    if "disabled" in t.get_attribute("class"):
                        sizes.append("{}(Agotado)".format(t.find_element_by_xpath("./div/div/span").get_attribute("innerText")))
                    else:
                        sizes.append(t.find_element_by_xpath("./div/div/span").get_attribute("innerText"))
                allSizes.append(sizes)
                images = []
                thumbnails = self.driver.find_elements_by_xpath(xpaths['thumbnails'])
                for i in range(len(thumbnails)):
                    mouse.move_to_element(thumbnails[i]).perform()
                    thumbnails[i].click()
                for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                    if not 'transparent-background' in i.get_attribute("src"):
                        images.append(i.get_attribute("src"))
                        print(i.get_attribute("src"))
                allImages.append(images)
                colors.append(colorsBtn[c].get_attribute("innerText").replace("Color: ", "").replace('"', "").capitalize())
                colorsBtn = self.driver.find_elements_by_xpath('.//ul[@class="product-detail-info-color-selector__colors"]/li/button')
            db.add(Item(brand,name,description,priceBfr,[priceNow],discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale, self.gender))
        except Exception as e:
            i = 0
            print('Item saltado\n',url,e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

# Main Code
# ScrapZara()