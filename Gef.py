from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Item import Item
from Database import Database
brand = "Gef"

class ScrapGef:
    def __init__(self):
        '''options = Options()
        options.add_argument("user-data-dir=./Cookies/Gef")
        options.add_argument("enable-automation")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome("./chromedriver.exe",options=options)'''
        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.db = Database(brand)
        self.driver.maximize_window()
        self.driver.get("https://www.gef.com.co/tienda/es-co/gef?gclid=EAIaIQobChMI2bDutMa47gIVFInICh1RYwQgEAAYASAAEgKDfvD_BwE")
        categories = [self.driver.find_elements_by_xpath('.//div[@class="header"]/a[@class="menuLink" and not(contains(@data-open,"nuevo")) and not(contains(@data-open,"green")) and not(contains(@data-open,"bono"))and not(contains(@data-open,"sale2")) ]'),[]]
        for c in categories[0]:
            categories[1].append(c.get_attribute('data-open'))
            categories[0][categories[0].index(c)] = c.get_attribute("textContent").replace('/',', ').replace('¡','').replace('!','').capitalize()
        for c in categories[1]:
            if "gef/mujeres" in c:
                self.gender = 'Mujer'
            elif "gef/gef-men" in c:
                self.gender = 'Hombre'
            elif "gef/junior" in c:
                self.gender = 'Niños'
            self.category = categories[0][categories[1].index(c)]
            self.subcategory = self.category
            self.scrapCategory(c)

    def scrapCategory(self, url):
        self.driver.get(url)
        loading = True
        elems = self.driver.find_elements_by_xpath('.//div[@class="listProductTienda"]/div/div/a')
        while loading:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            loading = len(elems) < len(self.driver.find_elements_by_xpath('.//div[@class="listProductTienda"]/div/div/a'))
            elems = self.driver.find_elements_by_xpath('.//div[@class="listProductTienda"]/div/div/a')
        for e in range(len(elems)):
            self.driver.execute_script("arguments[0].scrollIntoView();", elems[e])
            self.db.addUrl(elems[e].get_attribute('href'))
            if not self.db.contains(elems[e].get_attribute('href')):
                try:
                    self.subcategory = self.driver.find_element_by_xpath('.//li[@class="current"]').text.capitalize().replace('/',', ')
                    self.scrapProduct(elems[e].get_attribute("href"))
                except:
                    elems = self.driver.find_elements_by_xpath('.//div[@class="listProductTienda"]/div/div/a')
                    self.subcategory = self.driver.find_element_by_xpath('.//li[@class="current"]').text.capitalize()
                    self.scrapProduct(elems[e].get_attribute("href"))

    def scrapProduct(self, url):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            sleep(3)
            name = self.driver.find_element_by_xpath('.//h1[@class="main_header"]').text.capitalize()
            if not name:
                sleep(3)
                name = self.driver.find_element_by_xpath('.//h1[@class="main_header"]').text.capitalize()
            try:
                description = self.driver.find_element_by_xpath('.//div[contains(@id,"product_longdescription")]').text
            except:
                description = " "
            colorsBtn = self.driver.find_elements_by_xpath('.//div[@class="color_swatch_list"]/ul/li/a/img')
            comunName = []
            skipName=[[],[]]
            colors = []
            allSizes = []
            allImages = []
            allPricesNow = []
            allPricesBfr = []
            for c in range(len(colorsBtn)):
                name = self.driver.find_element_by_xpath('.//h1[@class="main_header"]').text.capitalize()
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
                colorsBtn[c].click()
                try:
                    priceNow = self.driver.find_element_by_xpath('.//span[@class="price"]').text
                    priceBfr = ' '
                except:
                    try:
                        priceNow = self.driver.find_element_by_xpath('.//span[@class="price diff"]').text
                        priceBfr = self.driver.find_element_by_xpath('.//span[@class="old_price"]').text
                    except:
                        priceNow = "$"
                if not priceNow:
                    priceNow = "$"
                allPricesNow.append(priceNow)
                allPricesBfr.append(priceBfr)
                colors.append(colorsBtn[c].get_attribute("src"))
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath('.//div[@class="color_swatch_list"]/ul[@aria-label="TALLA"]/li/a')
                for s in sizesTags:
                    if "disabled_enable" in s.find_element_by_xpath("./div").get_attribute("class"):
                        sizes.append("{}(Agotado)".format(s.find_element_by_xpath("./span").get_attribute("innerText")))
                    else:
                        sizes.append(s.find_element_by_xpath("./span").get_attribute("innerText"))
                if len(sizesTags) == 0:
                    sizes.append("Única")
                allSizes.append(sizes)
                images = []
                minis = self.driver.find_elements_by_xpath('.//ul[@id="ProductAngleImagesAreaList"]/li')
                if 'none' in self.driver.find_element_by_xpath('.//div[@class="other_views nodisplay"]').get_attribute('style'):
                    images.append(self.driver.find_element_by_xpath('.//img[@id="productMainImage"]').get_attribute("src"))
                else:
                    for i in range(len(minis)):
                        minis[0].click()
                        src = self.driver.find_element_by_xpath('.//img[@id="productMainImage"]').get_attribute("src")
                        if not src in images:
                            images.append(src)
                        self.driver.find_element_by_xpath('.//button[@id="top-btn"]').click()
                        minis = self.driver.find_elements_by_xpath('.//ul[@id="ProductAngleImagesAreaList"]/li')
                images.sort()
                allImages.append(images)
                colorsBtn = self.driver.find_elements_by_xpath('.//div[@class="color_swatch_list"]/ul/li/a/img')
            name = " ".join(comunName)
            w = skipName[0][skipName[1].index(max(skipName[1]))]
            if not name.startswith(w):
                name = " ".join([w,name])
            if name:
                self.sale = False
                self.db.add(Item(brand,name,description,allPricesBfr,allPricesNow,' ',allImages,url,allSizes,colors,self.category,self.category, self.subcategory,self.subcategory,self.gender))
            else:
                print("Hubo un error")
        except Exception as e:
            self.db.urlError(url)
            print("Item saltado")
            print(e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


# Main Code
#ScrapGef()