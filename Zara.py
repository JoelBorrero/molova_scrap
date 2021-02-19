import os
from time import sleep
from selenium import webdriver
from Item import Item


class ScrapZara:
    def __init__(self):
        self.brand = "Zara"
        self.sale = False
        if not os.path.exists("{}/".format(self.brand)):
            os.mkdir("{}/".format(self.brand))
        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.driver.maximize_window()
        # Scrap categorías
        self.driver.get("https://www.zara.com/co/")        
        exclusions = ["c325501","hombre-c84","l267","l286","l304","l394","l439","l450","l469","l769","l1003","l1024","l1119","l1066","l1184","l1217","l1251","l1253","l1299","l1335","l1362","l1977","l2975",]
        # "l1114"
        i=0
        cats=[[],[]]
        for cat in self.driver.find_elements_by_xpath('.//ul[@class="layout-categories__container"]/li/ul/li[not(contains(@class,"divider"))]//ul/li/a'):
            c = cat.get_attribute('innerText').capitalize()
            if not cat.get_attribute("href") in cats[1] and not 'Ver todo' in c and not 'Divider_menu' in c:
                cats[0].append(c)
                cats[1].append(cat.get_attribute("href"))
        for i in range(len(cats[0])):
            self.category = cats[0][i]
            self.originalCategory = self.category
            print(cats[1][i])
            if 'rebajas' in cats[1][i]:
                self.sale = True
            else:
                self.sale = False
            if 'mujer' in cats[1][i] or 'woman' in cats[1][i]:
                self.gender = 'Mujer'
                self.scrapCategoria(cats[1][i])
            elif 'hombre' in cats[1][i]:
                self.gender = 'Hombre'
                self.scrapCategoria(cats[1][i])

    def scrapCategoria(self, url):
        loading = False     #Testing
        self.driver.get(url)
        try:
            self.subcategory = self.driver.find_element_by_xpath('.//span[@class="category-topbar-related-categories__category-name category-topbar-related-categories__category-name--selected"]').text.capitalize()
        except:
            self.subcategory = self.category
        if self.subcategory != 'Ver todo':
            self.originalSubcategory = self.subcategory
            itemsWebElems = self.driver.find_elements_by_class_name("product-grid-product")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            while loading:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(3)
                loading = len(itemsWebElems) < len(self.driver.find_elements_by_class_name("product-grid-product"))
                itemsWebElems = self.driver.find_elements_by_xpath('.//li[@class="product-grid-block"]/ul/li')
            for i in itemsWebElems[:1]:
                try:
                    i = i.find_element_by_xpath("./a")
                    self.driver.execute_script("arguments[0].scrollIntoView();", i)
                    self.scrapProduct(i.get_attribute("href"))
                except Exception as e:
                    print(e)

    def scrapProduct(self, url):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            name = self.driver.find_element_by_xpath('.//h1[@class="product-detail-info__name"]').text.capitalize()
            description = self.driver.find_element_by_xpath('.//div[@class="expandable-text__inner-content"]/p').text.capitalize()
            try:
                priceBfr = self.driver.find_element_by_xpath('.//div[@class="product-detail-info__price-amount price"]/span[@class="price__amount price__amount--old"]').text
                priceNow = self.driver.find_element_by_xpath('.//div[@class="product-detail-info__price-amount price"]/span[@class="price__amount price__amount--on-sale"]').text
                discount = self.driver.find_element_by_xpath('.//div[@class="product-detail-info__price-amount price"]/span[@class="price__amount price__amount--on-sale"]/span').get_attribute('innerText')
            except:
                priceBfr = self.driver.find_element_by_xpath('.//span[@class="price__amount"]').text
                priceNow = priceBfr
                discount = ''
            otherColors = self.driver.find_elements_by_xpath('.//ul[@class="product-detail-info-color-selector__colors"]/li/button')
            colors = []
            allSizes = []
            allImages = []
            if len(otherColors) == 0:
                try:
                    color = self.driver.find_element_by_xpath('.//p[@class="product-detail-info-color-selector__selected-color-name"]')
                except:
                    color = self.driver.find_element_by_xpath('.//p[@class="product-detail-info__color"]')
                colors.append(color.text.replace("Color: ", "").replace('"', "").capitalize())
                tallas = []
                for t in self.driver.find_elements_by_xpath('.//ul[@id="product-size-selector-product-detail-info-83842347-menu"]/li'):
                    if "disabled" in t.get_attribute("class"):
                        tallas.append("{}(Agotado)".format(t.find_element_by_xpath("./div/div/span").get_attribute("innerText")))
                    else:
                        tallas.append(t.find_element_by_xpath("./div/div/span").get_attribute("innerText"))
                        tallas.append(t.find_element_by_xpath("./div/div").get_attribute("innerText"))
                        tallas.append(t.find_element_by_xpath("./div").get_attribute("innerText"))
                        tallas.append(t.get_attribute("innerText"))
                allSizes.append(tallas)
                images = []
                for i in self.driver.find_elements_by_xpath('.//div[@class="media__wrapper media__wrapper--fill media__wrapper--force-height"]/picture/img[@class="media-image__image media__wrapper--media"]'):
                    images.append(i.get_attribute("src"))
                allImages.append(images)
            for c in range(len(otherColors)):
                otherColors[c].click()
                sleep(2)
                tallas = []
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
            Item(self.brand,name,description,priceBfr,[priceNow],discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale, self.gender)
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
ScrapZara()