from time import sleep
from Database import Database
from selenium import webdriver
from Item import Item
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

xpaths={
    'categories':'.//li[contains(@class,"has-new-products-count")]/a',
    'categoriesSale':'.//ul[@class="product-categories"]/li/*[1]',
    'colorsBtn':'.//div[@class="c-product-info--header"]/div[contains(@class,"product-card-color-selector")]/div/div/div/img',
    'description':'.//span[@class="c-product-info--description-text"]',
    'discount':'./../..//div[@class="product-price--price product-price--price-discount"]',
    'elems':'.//div[@class="new-category-page tiles-list tiles-list--halves-grid"]/div/div/div[@id="productWrapper" or @class="carousel-wrapper carousel-wrapper--landscape"]/a',
    'imgs':'.//div[@id="product-grid"]/div/div/figure/img',
    'name':'.//h1[@class="title"]',
    'priceBfr':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div[@class="price price-old"]/span',
    'priceNow':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div[@class="sale"]/span',
    'priceNow2':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div/span',
    'sizesTags':'.//div[@class="c-product-info--size"]/div/div/div[@class="product-card-size-selector--dropdown-sizes"]/div',
    'subCats':'.//div[starts-with(@class,"carrousel-filters")]/div/div/div/div',
    'subCats2':'.//div[@class="category-badges-list"]/a[not(text()="Ver todo")]'}

class ScrapPullAndBear:
    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.set_page_load_timeout(30)
        self.brand = "Pull & Bear"
        self.db = Database(self.brand)
        self.driver.maximize_window()
        self.sale = False
        self.visitedIds = []
        self.scrapSaleAndNew()
        self.gender = "Mujer"
        self.scrapGender("https://www.pullandbear.com/co/mujer-c1030204557.html")
        self.gender = "Hombre"
        # self.scrapGender("https://www.pullandbear.com/co/hombre-c1030204558.html")
        self.driver.close()

    def scrapSaleAndNew(self):
        self.sale = True
        self.gender = 'Mujer'
        for i in ['https://www.pullandbear.com/co/mujer-c1030006518.html']:#,'https://www.pullandbear.com/co/hombre-c1030204558.html']:
            self.driver.get(i)
            print('Will wait')
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, xpaths["categoriesSale"])))
            except:
                print('Waited')
            categories = [self.driver.find_elements_by_xpath(xpaths['categoriesSale']),[]]
            print(categories[0])
            for c in categories[0]:
                cat = c.get_attribute("innerText").replace("\n", "")
                categories[1].append(c.get_attribute("href"))
                while cat.startswith(" "):
                    cat = cat[1:]
                while cat.endswith(" "):
                    cat = cat[:-1]
                categories[0][categories[0].index(c)] = cat
            print(categories[0])
            for c in range(len(categories[0])):
                self.category = categories[0][c]
                self.originalCategory = categories[0][c]
                self.scrapCategory(categories[1][c])
            # self.gender = 'Hombre'
        self.sale = False
        
    def scrapGender(self, url):
        self.driver.get(url)
        categories = [self.driver.find_elements_by_xpath(xpaths['categories']),[]]
        while not categories[0]:
            sleep(1)
            categories = [self.driver.find_elements_by_xpath(xpaths['categories']),[]]
        for c in categories[0]:
            cat = c.get_attribute("innerText").replace("\n", "")
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
        subCats = self.driver.find_elements_by_xpath(xpaths['subCats'])
        type = 1
        if not subCats:
            sleep(5)
            subCats = self.driver.find_elements_by_xpath(xpaths['subCats'])
            if not subCats:
                subCats = [self.driver.find_elements_by_xpath(xpaths['subCats2']),[]]
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
                    subCats = self.driver.find_elements_by_xpath(xpaths['subCats'])
                    self.subcategory = subCats[i].find_element_by_xpath('.//p').text
                    if not self.subcategory:
                        self.subcategory = (subCats[i].find_element_by_xpath('.//p').get_attribute("innerText"))
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
        elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        while loading:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            loading = len(elems) < len(self.driver.find_elements_by_xpath(xpaths['elems']))
            elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        for e in elems:
            self.driver.execute_script("arguments[0].scrollIntoView();", e)
            try:
                discount = self.driver.find_element_by_xpath(xpaths['discount'])
            except:
                discount = ' '
            self.db.addUrl(e.get_attribute("href"))
            if self.db.getIdByUrl not in self.visitedIds:
                # print(e.get_attribute("href"),discount)
                self.scrapProduct(e.get_attribute("href"),discount)
            else:
                print('Visitado ya ',e.get_attribute("href"))

    def scrapProduct(self, url, discount):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            try:
                name = self.driver.find_element_by_xpath(xpaths['name']).text
            except:
                sleep(3)
                name = self.driver.find_element_by_xpath(xpaths['name']).text
            description = self.driver.find_element_by_xpath(xpaths['description']).text
            try:
                priceNow = self.driver.find_element_by_xpath(xpaths['priceNow']).text
            except:
                priceNow = self.driver.find_element_by_xpath(xpaths['priceNow2']).text
            try:
                priceBfr = self.driver.find_element_by_xpath(xpaths['priceBfr']).text
            except:
                priceBfr = priceNow
            colorsBtn = self.driver.find_elements_by_xpath(xpaths['colorsBtn'])
            colors = []
            allSizes = []
            allImages = []
            for c in colorsBtn:
                c.click()
                colors.append(c.get_attribute("src"))
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath(xpaths['sizesTags'])
                for s in sizesTags:
                    if "disabled" in s.get_attribute("class"):
                        sizes.append("{}(Agotado)".format(s.get_attribute("innerText")))
                    else:
                        sizes.append(s.get_attribute("innerText"))
                if not sizesTags:
                    sizes = ["Única"]
                allSizes.append(sizes)
                images = []
                imgs = self.driver.find_elements_by_xpath(xpaths['imgs'])
                for i in range(len(imgs)):
                    while not imgs[i].get_attribute("src"):
                        self.driver.execute_script("arguments[0].scrollIntoView();", imgs[i])
                        imgs = self.driver.find_elements_by_xpath(xpaths['imgs'])
                        sleep(1)
                    images.append(imgs[i].get_attribute("src"))
                allImages.append(images)
            self.visitedIds.append(self.db.add(Item(self.brand,name,description,priceBfr,priceNow,discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale,self.gender)))
            if len(self.visitedIds >20):
                self.visitedIds.pop(0)
            print(self.visitedIds)
        except Exception as e:
            print("Item saltado:",e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


# Main Code
# ScrapPullAndBear()