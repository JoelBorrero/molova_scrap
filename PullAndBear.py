import random, json, os
from time import sleep
from selenium import webdriver
from Item import Item
from selenium.webdriver.chrome.options import Options


class ScrapPullAndBear:
    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.brand = "Pull & Bear"
        if not os.path.exists("{}/".format(self.brand)):
            os.mkdir("{}/".format(self.brand))
        self.driver.maximize_window()
        self.scrapSale()
        self.gender = "Mujer"
        self.scrapGender("https://www.pullandbear.com/co/mujer-c1030204557.html")
        self.gender = "Hombre"
        self.scrapGender("https://www.pullandbear.com/co/hombre-c1030204558.html")

    def scrapSale(self):
        self.sale = True
        self.gender = 'Mujer'
        for i in ['https://www.pullandbear.com/co/mujer-c1030204557.html','https://www.pullandbear.com/co/hombre-c1030204558.html']:
            self.driver.get(i)
            categories = [self.driver.find_elements_by_xpath('.//ul[@class="subitems"]/li/ul/li'),[]]
            while not categories[0]:
                sleep(1)
                categories = [self.driver.find_elements_by_xpath('.//ul[@class="subitems"]/li/ul/li'),[]]
            for c in categories[0]:
                cat = c.get_attribute("innerText").replace("\n", "")
                categories[1].append(c.find_element_by_xpath('./a').get_attribute("href"))
                while cat.startswith(" "):
                    cat = cat[1:]
                while cat.endswith(" "):
                    cat = cat[:-1]
                categories[0][categories[0].index(c)] = cat
            for c in categories[0][:16]:
                self.category = c
                self.originalCategory = c
                self.scrapCategory(categories[1][categories[0].index(c)])
            self.gender = 'Hombre'
        self.sale = False
        
    def scrapGender(self, url):
        self.driver.get(url)
        categories = [self.driver.find_elements_by_xpath('.//ul[@class="product-categories"]/li/ul/li/a[not(contains(@href,"rebajas")) and not(contains(@href,"ver-todo")) and not(contains(@href,"novedades"))]'),[]]
        while not categories[0]:
            sleep(1)
            categories = [self.driver.find_elements_by_xpath('.//ul[@class="product-categories"]/li/ul/li/a[not(contains(@href,"rebajas")) and not(contains(@href,"ver-todo")) and not(contains(@href,"novedades"))]'),[]]
        for c in categories[0]:
            cat = c.get_attribute("innerText").replace("\n", "")
            if not "Ver todo" in cat:
                categories[1].append(c.get_attribute("href"))
                while cat.startswith(" "):
                    cat = cat[1:]
                while cat.endswith(" "):
                    cat = cat[:-1]
                categories[0][categories[0].index(c)] = cat
        for c in categories[0]:
            self.category = c
            self.originalCategory = c
            self.scrapCategory(categories[1][categories[0].index(c)])

    def scrapCategory(self, url):
        self.driver.get(url)
        subCats = self.driver.find_elements_by_xpath('.//div[starts-with(@class,"carrousel-filters")]/div/div/div/div')
        type = 1
        if not subCats:
            sleep(5)
            subCats = self.driver.find_elements_by_xpath('.//div[starts-with(@class,"carrousel-filters")]/div/div/div/div')
            if not subCats:
                subCats = [self.driver.find_elements_by_xpath('.//div[@class="category-badges-list"]/a[not(text()="Ver todo")]'),[]]
                if subCats[0]:
                    i = 0
                    for s in subCats[0]:
                        i = subCats[0].index(s)
                        subCats[1].append(subCats[0][i].get_attribute("href"))
                        subCats[0][i] = subCats[0][i].get_attribute("innerText")
                    if not subCats[0][i]:
                        subCats[0][i] = subCats[0][i].text
                    type = 2
                else:
                    type = 3
        for i in range(len(subCats)):
            if type == 1:
                if not "Ver Todo" in subCats[i].get_attribute("innerText"):
                    subCats = self.driver.find_elements_by_xpath('.//div[@class="c-tile c-tile--product c-tile--product-fullwidth-fullheight c-tile--product--carousel-option"]/div[@class="product-info"]')
                    self.subcategory = (subCats[i].find_element_by_xpath('.//span[@class="product-name"]').text)
                    if not self.subcategory:
                        self.subcategory = (subCats[i].find_element_by_xpath('.//span[@class="product-name"]').get_attribute("innerText"))
                    self.driver.execute_script("arguments[0].scrollIntoView();", subCats[i])
                    subCats[i].find_element_by_xpath("./div").click()
                    sleep(3)
                    self.originalSubcategory = self.subcategory
                    self.scrapSubcategory("")
            elif type == 2:
                self.subcategory = subCats[0][i]
                self.originalSubcategory = self.subcategory
                self.scrapSubcategory(subCats[1][i])
            else:
                self.subcategory = self.category
                self.originalSubcategory = self.subcategory
                self.scrapSubcategory("")

    def scrapSubcategory(self, url):
        if url:
            self.driver.get(url)
            sleep(5)
        loading = True
        elems = self.driver.find_elements_by_xpath(
            './/div[@class="new-category-page tiles-list tiles-list--halves-grid"]/div/div/div[@id="productWrapper" or @class="carousel-wrapper carousel-wrapper--landscape"]/a'
        )
        while loading:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            sleep(3)
            loading = len(elems) < len(
                self.driver.find_elements_by_xpath(
                    './/div[@class="new-category-page tiles-list tiles-list--halves-grid"]/div/div/div[@id="productWrapper" or @class="carousel-wrapper carousel-wrapper--landscape"]/a'
                )
            )
            elems = self.driver.find_elements_by_xpath(
                './/div[@class="new-category-page tiles-list tiles-list--halves-grid"]/div/div/div[@id="productWrapper" or @class="carousel-wrapper carousel-wrapper--landscape"]/a'
            )
        for e in elems[:1]:
            self.driver.execute_script("arguments[0].scrollIntoView();", e)
            try:
                discount = self.driver.find_element_by_xpath('./../..//div[@class="product-price--price product-price--price-discount"]')
            except:
                discount = ' '
            self.scrapProduct(e.get_attribute("href"),discount)

    def scrapProduct(self, url, discount):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            try:
                name = self.driver.find_element_by_xpath('.//h1[@class="title"]').text
            except:
                sleep(3)
                name = self.driver.find_element_by_xpath('.//h1[@class="title"]').text
            description = self.driver.find_element_by_xpath(
                './/span[@class="c-product-info--description-text"]'
            ).text
            try:
                priceNow = self.driver.find_element_by_xpath('.//div[@class="c-product-info--header"]/div[@class="prices"]/div[@class="sale"]/span').text
            except:
                priceNow = self.driver.find_element_by_xpath('.//div[@class="c-product-info--header"]/div[@class="prices"]/div/span').text
            try:
                priceBfr = self.driver.find_element_by_xpath('.//div[@class="c-product-info--header"]/div[@class="prices"]/div[@class="price price-old"]/span').text
            except:
                priceBfr = priceNow
            colorsBtn = self.driver.find_elements_by_xpath(
                './/div[@class="c-product-info--header"]/div[contains(@class,"product-card-color-selector")]/div/div/div/img'
            )
            colors = []
            allSizes = []
            allImages = []
            for c in colorsBtn:
                c.click()
                colors.append(c.get_attribute("src"))
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath(
                    './/div[@class="c-product-info--size"]/div/div/div[@class="product-card-size-selector--dropdown-sizes"]/div'
                )
                for s in sizesTags:
                    if "disabled" in s.get_attribute("class"):
                        sizes.append("{}(Agotado)".format(s.get_attribute("innerText")))
                    else:
                        sizes.append(s.get_attribute("innerText"))
                if not sizesTags:
                    sizesTag = ["Única"]
                allSizes.append(sizes)
                images = []
                imgs = self.driver.find_elements_by_xpath(
                    './/div[@id="product-grid"]/div/div/figure/img'
                )
                for i in range(len(imgs)):
                    while not imgs[i].get_attribute("src"):
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView();", imgs[i]
                        )
                        imgs = self.driver.find_elements_by_xpath(
                            './/div[@id="product-grid"]/div/div/figure/img'
                        )
                        sleep(1)
                    images.append(imgs[i].get_attribute("src"))
                allImages.append(images)
            Item(self.brand,name,description,priceBfr,priceNow,discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale,self.gender)
        except Exception as e:
            print("Item saltado")
            print(e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


# Main Code
ScrapPullAndBear()