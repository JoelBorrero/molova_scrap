import os, Database
from Item import Item
from time import sleep
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options

class ScrapZara:
    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.brand = "Zara"
        self.db = Database.Database(self.brand)
        self.sale = False
        self.driver.maximize_window()
        self.driver.get("https://www.zara.com/co/")
        cats=[[],[]]
        sales = [[],[],['?v1=1713916','?v1=1713384','?v1=1713588','?v1=1713959','?v1=1714113','?v1=1714042','?v1=1714238','?v1=1714298']]
        for cat in self.driver.find_elements_by_xpath('.//ul[@class="layout-categories__container"]/li[position()<3]/ul/li[not(contains(@class,"divider"))]/ul/li/a'):
            c = cat.get_attribute('innerText').capitalize()
            if 'Special prices' in c:
                sales[0].append(c)
                sales[1].append(cat.get_attribute("href"))
            else:
                cats[0].append(c)
                cats[1].append(cat.get_attribute("href"))
        self.sale = True
        i=0
        for i in range(len(sales[0])):
            self.category = sales[0][i]
            self.originalCategory = self.category
            if 'mujer' in sales[1][i] or 'woman' in sales[1][i]:
                self.gender = 'Mujer'
            else:
                self.gender = 'Hombre'
            self.scrapCategoria(sales[1][i])
        self.sale = False
        i=0
        for i in range(len(cats[0])):
            self.category = cats[0][i]
            self.originalCategory = self.category
            if 'mujer' in cats[1][i] or 'woman' in cats[1][i]:
                self.gender = 'Mujer'
            else:
                self.gender = 'Hombre'
            self.scrapCategoria(cats[1][i])

    def scrapCategoria(self, url):
        self.driver.get(url)
        try:
            self.subcategory = self.driver.find_element_by_xpath('.//span[@class="category-topbar-related-categories__category-name category-topbar-related-categories__category-name--selected"]').text.capitalize()
        except:
            self.subcategory = self.category
        subcats = self.driver.find_elements_by_xpath('.//li[@class="variable-width-carousel__item"]/a/div/span')
        if subcats:
            for s in range(len(subcats)):
                subcats = self.driver.find_elements_by_xpath('.//li[@class="variable-width-carousel__item"]/a/div/span')
                if subcats[s].text.lower() != 'ver todo':
                    try:
                        subcats[s].click()
                        sleep(5)
                        self.subcategory = self.driver.find_element_by_xpath('.//span[@class="category-topbar-related-categories__category-name category-topbar-related-categories__category-name--selected"]').text.capitalize()
                        self.scrapSubcategory()
                    except:
                        try:
                            self.driver.find_element_by_xpath('.//button[@class="variable-width-carousel__arrow variable-width-carousel__arrow--right"]').click()
                            subcats[s].click()
                            sleep(5)
                            self.subcategory = self.driver.find_element_by_xpath('.//span[@class="category-topbar-related-categories__category-name category-topbar-related-categories__category-name--selected"]').text.capitalize()
                            self.scrapSubcategory()
                        except:
                            print('Never click')
        else:
            self.scrapSubcategory()
            
    def scrapSubcategory(self):
        loading = True     #Testing
        self.originalSubcategory = self.subcategory
        xpath = './/li[@class="product-grid-block"]/ul/li/a'
        itemsWebElems = self.driver.find_elements_by_xpath(xpath)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        while loading:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            loading = len(itemsWebElems) < len(self.driver.find_elements_by_xpath(xpath))
            itemsWebElems = self.driver.find_elements_by_xpath(xpath)
        for i in itemsWebElems:
            try:
            #     try:
            #         i = i.find_element_by_xpath("./a")
            #     except Exception as e:
            #         i = i.find_element_by_xpath("./ul/li/a")
            #     self.driver.execute_script("arguments[0].scrollIntoView();", i)   
                
                self.db.addUrl(i.get_attribute('href'))
                if not self.db.contains(i.get_attribute('href')):
                    self.scrapProduct(i.get_attribute('href'))
            except:
                self.db.urlError(i.get_attribute('href'))


    def scrapProduct(self, url):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            name = self.driver.find_element_by_xpath('.//h1[@class="product-detail-info__name"]').text.capitalize()
            description = self.driver.find_element_by_xpath('.//div[@class="expandable-text__inner-content"]/p').text.capitalize()
            try:
                priceBfr = self.driver.find_element_by_xpath('.//div[@class="product-detail-info__price-amount price"]/span[@class="price__amount price__amount--old"]').text
                priceNow = self.driver.find_element_by_xpath('.//div[@class="product-detail-info__price-amount price"]/span[@class="price__amount price__amount--on-sale"]').text
                try:
                    priceNow = priceNow[:priceNow.index('\n')]
                except:
                    try:
                        priceNow = priceNow[:priceNow.index('-')]
                    except:
                        priceNow = priceNow[:-3]
                discount = self.driver.find_element_by_xpath('.//div[@class="product-detail-info__price-amount price"]/span[@class="price__amount price__amount--on-sale"]/span').get_attribute('innerText')
            except:
                priceBfr = self.driver.find_element_by_xpath('.//span[@class="price__amount"]').text
                priceNow = priceBfr
                discount = ' '
            otherColors = self.driver.find_elements_by_xpath('.//ul[@class="product-detail-info-color-selector__colors"]/li/button')
            colors = []
            allSizes = []
            allImages = []
            if len(otherColors) == 0:
                try:
                    color = self.driver.find_element_by_xpath('.//p[@class="product-detail-info-color-selector__selected-color-name"]')
                except:
                    try:
                        color = self.driver.find_element_by_xpath('.//p[@class="product-detail-info__color"]')
                    except:
                        color = self.driver.find_element_by_xpath('.//p[@class="product-detail-color-selector__selected-color-name"]')
                colors.append(color.text.replace("Color: ", "").replace('"', "").capitalize())
                tallas = []
                for t in self.driver.find_elements_by_xpath('.//ul[contains(@id,"product-size-selector-product-detail-info-")]/li'):
                    if "disabled" in t.get_attribute("class"):
                        tallas.append("{}(Agotado)".format(t.find_element_by_xpath("./div/div/span").get_attribute("innerText")))
                    else:
                        tallas.append(t.find_element_by_xpath("./div/div/span").get_attribute("innerText"))
                allSizes.append(tallas)
                images = []
                for i in self.driver.find_elements_by_xpath('.//div[@class="media__wrapper media__wrapper--fill media__wrapper--force-height"]/picture/img[@class="media-image__image media__wrapper--media"]'):
                    images.append(i.get_attribute("src"))
                allImages.append(images)
            for c in range(len(otherColors)):
                otherColors[c].click()
                tallas = []
                while not self.driver.find_elements_by_xpath('.//ul[contains(@id,"product-size-selector-product-detail-info")]/li'):
                    sleep(0.1)
                for t in self.driver.find_elements_by_xpath('.//ul[contains(@id,"product-size-selector-product-detail-info")]/li'):
                    if "disabled" in t.get_attribute("class"):
                        tallas.append("{}(Agotado)".format(t.find_element_by_xpath("./div/div/span").get_attribute("innerText")))
                    else:
                        tallas.append(t.find_element_by_xpath("./div/div/span").get_attribute("innerText"))
                allSizes.append(tallas)
                images = []
                for i in self.driver.find_elements_by_xpath('.//div[@class="media__wrapper media__wrapper--fill media__wrapper--force-height"]/picture/img[@class="media-image__image media__wrapper--media"]'):
                    images.append(i.get_attribute("src"))
                allImages.append(images)
                colors.append(otherColors[c].get_attribute("innerText").replace("Color: ", "").replace('"', "").capitalize())
                otherColors = self.driver.find_elements_by_xpath('.//ul[@class="product-detail-info-color-selector__colors"]/li/button')
            self.db.add(Item(self.brand,name,description,priceBfr,[priceNow],discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale, self.gender))
        except Exception as e:
            i = 0
            if not os.path.exists("Errors/{}".format(self.brand)):
                os.mkdir("Errors/{}".format(self.brand))
            while os.path.exists('Errors/{}/{}{}.png'.format(self.brand, e, i)):
                i = i + 1
            self.driver.save_screenshot('Errors/{}/{}{}.png'.format(self.brand, e, i))
            print("Item saltado")
            print(e)
            #input('Continuar?')
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

# Main Code
#ScrapZara()