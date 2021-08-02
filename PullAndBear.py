from time import sleep
from Database import Database
from selenium import webdriver
from Item import Item
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

brand = 'Pull & Bear'
db = Database(brand)
xpaths={
    'categories':'.//ul[@class="product-categories"]/li/ul/li/a',
    'categoriesSale':'.//ul[@class="product-categories"]/li[contains(@class,"sale")]/ul/li/a',
    'colorsBtn':'.//div[@class="c-product-info--header"]/div[contains(@class,"product-card-color-selector")]/div/div/div/img',
    'description':'.//span[@class="c-product-info--description-text"]',
    'discount':'./../..//div[@class="product-price--price product-price--price-discount"]',
    'elems':'.//div[@class="c-tile c-tile--product"][div/a]',
    'fast_discount': './div/div/div[@class="discount"]',
    'fast_image': './div/a/div/div/figure/img',
    'fast_price':'./div[@class="product-info"]/div[@class="price-container"]/div/div[@class="product-price--price"]',
    'fast_priceBfr': './div[@class="product-info"]/div[@class="price-container"]/div/div[contains(@class,"old")]',
    'fast_priceNow': './div[@class="product-info"]/div[@class="price-container"]/div/div[contains(@class,"sale")]',
    'href':'./div/a',
    'imgs':'.//div[@id="product-grid"]/div/div/figure/img',
    'name':'.//h1[@class="title"]',
    'priceBfr':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div[@class="price price-old"]/span',
    'priceNow':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div[@class="sale"]/span',
    'priceNow2':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div/span',
    'sizesTags':'.//div[@class="c-product-info--size"]/div/div/div[@class="product-card-size-selector--dropdown-sizes"]/div',
    'subCats':'.//div[starts-with(@class,"carrousel-filters")]/div/div/div/div',
    'subCats2':'.//div[@class="category-badges-list"]/button[not(@value="Ver todo")][span]'}

class ScrapPullAndBear:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.set_page_load_timeout(30)
        self.driver.maximize_window()
        self.gender = 'Mujer'
        # self.ScrapSale()
        self.scrapGender('https://www.pullandbear.com/co/mujer-c1030204557.html')
        self.driver.quit()
        
    def ScrapSale(self):
        self.sale = True
        self.driver.get('https://www.pullandbear.com/co/mujer-c1030204557.html')
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpaths['categoriesSale'])))
        except:
            print('Waiting error')
        categories = [self.driver.find_elements_by_xpath(xpaths['categoriesSale']),[]]
        for c in categories[0]:
            cat = c.get_attribute('innerText').replace('\n', '')
            categories[1].append(c.get_attribute('href'))
            while cat.startswith(' '):
                cat = cat[1:]
            while cat.endswith(' '):
                cat = cat[:-1]
            categories[0][categories[0].index(c)] = cat
        for c in range(len(categories[0])):
            self.category = categories[0][c]
            self.originalCategory = categories[0][c]
            self.scrapCategory(categories[1][c])

    def updateProduct(self, elem):
        url = elem.find_element_by_xpath(xpaths['href']).get_attribute('href')
        try:
            priceBfr = elem.find_element_by_xpath(xpaths['fast_priceBfr']).text
            priceNow = elem.find_element_by_xpath(xpaths['fast_priceNow']).text
            discount = elem.find_element_by_xpath(xpaths['fast_discount']).text
        except:
            priceBfr = elem.find_element_by_xpath(xpaths['fast_price']).text
            priceNow = priceBfr
            discount = 0
        db.update_product(url, priceBfr, priceNow, discount)
        
    def scrapGender(self, url):
        self.sale = False
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
                subCats = self.driver.find_elements_by_xpath(xpaths['subCats2'])
                if subCats:
                    print(url,'type2')
                    type = 2#Text buttons
                    for button in subCats:
                        self.driver.find_element_by_xpath(".//body").send_keys(Keys.HOME)
                        sleep(1)
                        button.click()
                        sleep(3)
                        self.subcategory = button.find_element_by_xpath('./span').text
                        self.originalSubcategory = self.subcategory
                        self.scrapSubcategory()
                else:
                    print(url,'type3')
                    type = 3
        if subCats and type == 1:
            for i in range(len(subCats)):
                print(url,'type1')
                if not "Ver Todo" in subCats[i].get_attribute("innerText"):
                    subCats = self.driver.find_elements_by_xpath(xpaths['subCats'])
                    self.subcategory = subCats[i].find_element_by_xpath('.//p').text
                    if not self.subcategory:
                        self.subcategory = (subCats[i].find_element_by_xpath('.//p').get_attribute("innerText"))
                    # self.driver.execute_script("arguments[0].scrollIntoView();", subCats[i])
                    self.driver.find_element_by_xpath(".//body").send_keys(Keys.HOME)
                    try:
                        subCats[i].find_element_by_xpath("./div").click()
                    except:
                        self.driver.find_element_by_xpath('.//button[@class="flickity-button flickity-custom-prev-next-button next icon icon-flickity-next"]').click()
                        sleep(1)
                        try:
                            subCats[i].find_element_by_xpath("./div").click()
                        except:
                            self.driver.find_element_by_xpath('.//button[@class="flickity-button flickity-custom-prev-next-button next icon icon-flickity-next"]').click()
                            sleep(1)
                            try:
                                subCats[i].find_element_by_xpath("./div").click()
                            except:
                                self.driver.find_element_by_xpath('.//button[@class="flickity-button flickity-custom-prev-next-button next icon icon-flickity-next"]').click()
                                sleep(1)
                                subCats[i].find_element_by_xpath("./div").click()
                    sleep(3)
                    self.originalSubcategory = self.subcategory
                    self.scrapSubcategory()
        elif type == 3:
            self.subcategory = self.category
            self.originalSubcategory = self.subcategory
            self.scrapSubcategory()

    def scrapSubcategory(self, url=''):
        if url:
            self.driver.get(url)
            sleep(5)
        loading = True
        elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        while loading:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.find_element_by_xpath(".//body").send_keys(Keys.PAGE_UP)
            self.driver.find_element_by_xpath(".//body").send_keys(Keys.PAGE_UP)
            sleep(5)
            loading = len(elems) < len(self.driver.find_elements_by_xpath(xpaths['elems']))
            elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        for elem in elems:
            self.driver.execute_script("arguments[0].scrollIntoView();", elem)
            url = elem.find_element_by_xpath(xpaths['href']).get_attribute('href')
            image = elem.find_element_by_xpath(xpaths['fast_image']).get_attribute('src')
            if db.contains(url, image):
                self.updateProduct(elem)
            else:
                try:
                    discount = elem.find_element_by_xpath(xpaths['fast_discount']).text
                except:
                    discount = 0
                self.scrapProduct(url, discount)

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
            db.add(Item(brand,name,description,priceBfr,priceNow,discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale,self.gender))
        except Exception as e:
           print("Item saltado:",e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

# Main Code
# ScrapPullAndBear()