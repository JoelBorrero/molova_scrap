import os
from time import sleep
from selenium import webdriver
from Item import Item
from selenium.webdriver.chrome.options import Options

class ScrapBershka:
    def __init__(self):
        options = Options()
        options.add_argument("enable-automation")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        #self.driver = webdriver.Chrome("./chromedriver.exe",options=options)
        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.brand = "Bershka"
        if not os.path.exists("{}/".format(self.brand)):
            os.mkdir("{}/".format(self.brand))
        self.driver.maximize_window()
        self.scrapSale()
        self.scrapCategories("https://www.bershka.com/co/mujer-c1010193132.html")
        
    def scrapSale(self):
        h=0
        m=0
        self.driver.get('https://www.bershka.com/co/')
        self.sale = True
        categories = [[],[],self.driver.find_elements_by_xpath('.//li[@class="sub-menu-item custom-colored"]/a')]
        for c in categories[2]:
            cat = c.get_attribute("innerText").replace("\n", "")
            categories[1].append(c.get_attribute("href"))
            while cat.startswith(" "):
                cat = cat[1:]
            while cat.endswith(" "):
                cat = cat[:-1]
            categories[0].append(cat)
        for c in range(len(categories[0])):
            self.category = categories[0][c]
            self.originalCategory = self.category
            if 'hombre' in categories[1][c]:
                self.gender = 'Hombre'
                h+=1
            else:
                self.gender = 'Mujer'
                m+=1
            print('{}   :   {}'.format(categories[1][c][27:-5],c))
            self.scrapCategory(categories[1][c])
        print('{} cats, H:{}, M:{}'.format(len(categories[0]),h,m))
        self.sale = False

    def scrapCategories(self, url):
        h=0
        m=0
        self.driver.get(url)
        categories = [[],[],self.driver.find_elements_by_xpath('.//li[@class="sub-menu-item"]/a[not(contains(@href,"total-look")) and not(contains(@href,"join")) and not(contains(@href,"creators")) and not(@aria-label="Ir a Ver Todo")]')]
        for c in categories[2]:
            cat = c.get_attribute("innerText").replace("\n", "")
            categories[1].append(c.get_attribute("href"))
            while cat.startswith(" "):
                cat = cat[1:]
            while cat.endswith(" "):
                cat = cat[:-1]
            categories[0].append(cat)
        for c in categories[0]:
            self.category = c
            self.originalCategory = c
            if 'hombre' in categories[1][categories[0].index(c)]:
                self.gender = 'Hombre'
                h+=1
            else:
                self.gender = 'Mujer'
                m+=1
            print('{}   :   {}'.format(categories[1][categories[0].index(c)][27:-5],c))
        #print('{} cats, H:{}, M:{}'.format(len(categories[0]),h,m))
            self.scrapCategory(categories[1][categories[0].index(c)])

    def scrapCategory(self, url):
        self.driver.get(url)
        loading = False
        subCats = self.driver.find_elements_by_xpath('.//div[@class="filter-tag-swiper"]/div/ul/li')
        if not subCats:
            sleep(5)
            subCats = self.driver.find_elements_by_xpath('.//div[@class="filter-tag-swiper"]/div/ul/li')
        for s in range(len(subCats)):
            if not "Todas" in subCats[s].get_attribute("innerText"):
                try:
                    subCats[s].click()
                    self.subcategory = subCats[s].get_attribute('innerText')
                    self.originalSubcategory = subCats[s].get_attribute('innerText')
                    elems = self.driver.find_elements_by_xpath('.//ul[@class="grid-container"]/li/div/a')
                    while loading:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        sleep(3)
                        loading = len(elems) < len(self.driver.find_elements_by_xpath('.//ul[@class="grid-container"]/li/div/a'))
                        elems = self.driver.find_elements_by_xpath('.//ul[@class="grid-container"]/li/div/a')
                    for e in elems[:1]:
                        self.driver.execute_script("arguments[0].scrollIntoView();", e)
                        self.scrapProduct(e.get_attribute("href"))
                except:
                    print('Error clicking')
        if not subCats:
            self.subcategory = self.category
            self.originalSubcategory = self.category
            elems = self.driver.find_elements_by_xpath('.//ul[@class="grid-container"]/li/div/a')
            while loading:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(3)
                loading = len(elems) < len(self.driver.find_elements_by_xpath('.//ul[@class="grid-container"]/li/div/a'))
                elems = self.driver.find_elements_by_xpath('.//ul[@class="grid-container"]/li/div/a')
            for e in elems[:1]:
                self.driver.execute_script("arguments[0].scrollIntoView();", e)
                self.scrapProduct(e.get_attribute("href"))

    def scrapProduct(self, url):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            while not self.driver.find_elements_by_xpath('.//div/button/div[@class="image-item-wrapper"]/img'):
                sleep(1)
            name = self.driver.find_element_by_xpath('.//h1[@class="product-title"]').text
            description = self.driver.find_element_by_xpath('.//section[@class="product-info"]').text
            priceNow = self.driver.find_element_by_xpath('.//div[contains(@class,"current-price-elem")]').text
            try:
                priceBfr = self.driver.find_element_by_xpath('.//span[@class="old-price-elem"]').text
                discount = self.driver.find_element_by_xpath('.//span[@class="discount-tag"]').text
            except:
                priceBfr = priceNow
                discount = ' '
            colorsBtn = self.driver.find_elements_by_xpath('.//ul[@class="swiper-wrapper"]/li/a/div/img')
            colors = []
            allSizes = []
            allImages = []
            for c in colorsBtn:
                c.click()
                colors.append(c.get_attribute("src"))
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath('.//div[@class="sizes-list-detail"]/ul/li/button/span')
                for s in sizesTags:
                    if "disabled" in s.get_attribute("class"):
                        sizes.append("{}(Agotado)".format(s.get_attribute("innerText")))
                    else:
                        sizes.append(s.get_attribute("innerText"))
                if not sizes:
                    sizes = ["Única"]
                allSizes.append(sizes)
                images = []
                while not images:
                    sleep(1)
                    for i in self.driver.find_elements_by_xpath('.//div/button/div[@class="image-item-wrapper"]/img'):
                        images.append(i.get_attribute("src"))
                allImages.append(images)
            if not colorsBtn:
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath('.//div[@class="sizes-list-detail"]/ul/li/button/span')
                for s in sizesTags:
                    if "disabled" in s.get_attribute("class"):
                        sizes.append("{}(Agotado)".format(s.get_attribute("innerText")))
                    else:
                        sizes.append(s.get_attribute("innerText"))
                if not sizes:
                    sizes = ["Única"]
                allSizes.append(sizes)
                images = []
                while not images:
                    sleep(1)
                    for i in self.driver.find_elements_by_xpath('.//div/button/div[@class="image-item-wrapper"]/img'):
                        images.append(i.get_attribute("src"))
                allImages.append(images)
                colors.append(images[-2])
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
ScrapBershka()