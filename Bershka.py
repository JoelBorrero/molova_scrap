from Item import Item
from time import sleep
from Database import Database
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

xpaths = {
    "categories": './/li[@class="sub-menu-item"]/a[not(contains(@href,"total-look")) and not(contains(@href,"join")) and not(contains(@href,"creators")) and not(@aria-label="Ir a Ver Todo")]',
    "colorsBtn": './/ul[@class="swiper-wrapper"]/li/a/div/img',
    "coming": "./span/span/span",
    "description": './/section[@class="product-info"]',
    "discount": './/span[@class="discount-tag"]',
    "elems": './/ul[@class="grid-container"]/li/div/a',
    "images": './/div/button/div[@class="image-item-wrapper"]/img',
    "name": './/h1[@class="product-title"]',
    "priceBfr": './/span[@class="old-price-elem"]',
    "priceNow": './/div[contains(@class,"current-price-elem")]',
    "sale": ".//a[@style]",
    "sizesTags": './/div[@class="sizes-list-detail"]/ul/li/button',
    "subCats": './/div[@class="filter-tag-swiper"]/div/ul/li',
}


class ScrapBershka:
    def __init__(self):
        # options = Options()
        # options.add_argument("enable-automation")
        # options.add_argument("--headless")
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-extensions")
        # options.add_argument("--dns-prefetch-disable")
        # options.add_argument("--disable-gpu")
        # options.add_argument("user-data-dir=./Cookies/Bershka")
        # self.driver = webdriver.Chrome("./chromedriver.exe", options=options)
        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.driver.set_page_load_timeout(30)
        self.brand = "Bershka"
        self.db = Database(self.brand)
        self.driver.maximize_window()
        self.driver.get("https://www.bershka.com/co/")
        self.scrapSale()
        self.scrapCategories()
        self.driver.quit()

    def scrapSale(self):
        self.sale = True
        categories = [[], [], self.driver.find_elements_by_xpath(xpaths["sale"])]
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
            if "hombre" in categories[1][c]:
                self.gender = "Hombre"
            else:
                self.gender = "Mujer"
                self.scrapCategory(categories[1][c])
            # self.scrapCategory(categories[1][c])

    def scrapCategories(self):
        self.sale = False
        categories = [[], [], self.driver.find_elements_by_xpath(xpaths["categories"])]
        for c in categories[2]:
            cat = c.get_attribute("innerText").replace("\n", "")
            categories[1].append(c.get_attribute("href"))
            while cat.startswith(" "):
                cat = cat[1:]
            while cat.endswith(" "):
                cat = cat[:-1]
            categories[0].append(cat)
        categories[2].clear()
        for c in range(len(categories[0])):
            self.category = categories[0][c]
            self.originalCategory = categories[0][c]
            if "hombre" in categories[1][c]:
                self.gender = "Hombre"
            else:
                self.gender = "Mujer"
                self.scrapCategory(categories[1][c])

    def scrapCategory(self, url):
        self.driver.get(url)
        sleep(1)
        self.driver.find_element_by_xpath(".//body").send_keys(Keys.PAGE_DOWN)
        subCats = self.driver.find_elements_by_xpath(xpaths["subCats"])
        if not subCats:
            self.driver.find_element_by_xpath(".//body").send_keys(Keys.PAGE_DOWN)
            sleep(5)
            subCats = self.driver.find_elements_by_xpath(xpaths["subCats"])
        if subCats:
            for s in range(len(subCats)):
                if not "Todas" in subCats[s].get_attribute("innerText"):
                    try:
                        subCats[s].click()
                        self.driver.find_element_by_xpath(".//body").send_keys(
                            Keys.PAGE_DOWN
                        )
                        sleep(1)
                        subCats = self.driver.find_elements_by_xpath(xpaths["subCats"])
                        self.subcategory = subCats[s].get_attribute("innerText")
                        self.originalSubcategory = subCats[s].get_attribute("innerText")
                        self.scrapSubcategory()
                    except:
                        print("Error clicking")
        else:
            self.subcategory = self.category
            self.originalSubcategory = self.category
            self.scrapSubcategory()

    def scrapSubcategory(self):
        elems = [[], self.driver.find_elements_by_xpath(xpaths["elems"])]
        loading = True
        while loading:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            self.driver.find_element_by_xpath(".//body").send_keys(Keys.PAGE_UP)
            sleep(3)
            loading = len(elems[1]) < len(
                self.driver.find_elements_by_xpath(xpaths["elems"])
            )
            elems = [[], self.driver.find_elements_by_xpath(xpaths["elems"])]
        while elems[1]:
            e = elems[1].pop().get_attribute("href")
            e = e[: e.index(".html") + 5]
            self.db.addUrl(e)
            if not any(e[:-14] in el for el in elems[0]):
                elems[0].append(e)
        while elems[0]:
            self.scrapProduct(elems[0].pop())

    def scrapProduct(self, url):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            if not self.driver.find_elements_by_xpath(xpaths["images"]):
                sleep(1)
            name = self.driver.find_element_by_xpath(xpaths["name"]).text
            description = self.driver.find_element_by_xpath(xpaths["description"]).text
            priceNow = self.driver.find_element_by_xpath(xpaths["priceNow"]).text
            try:
                priceBfr = self.driver.find_element_by_xpath(xpaths["priceBfr"]).text
                discount = self.driver.find_element_by_xpath(xpaths["discount"]).text
            except:
                priceBfr = priceNow
                discount = "0"
            colorsBtn = self.driver.find_elements_by_xpath(xpaths["colorsBtn"])
            colors = []
            allSizes = []
            allImages = []
            for c in colorsBtn:
                try:
                    c.click()
                except:
                    sleep(2)
                    c.click()
                colors.append(c.get_attribute("src"))
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath(xpaths["sizesTags"])
                for s in sizesTags:
                    try:
                        s.find_element_by_xpath(xpaths["coming"])
                        sizes.append(
                            "{}(Próximamente)".format(s.get_attribute("innerText"))
                        )
                    except:
                        if "is-disabled" in s.get_attribute("class"):
                            sizes.append(
                                "{}(Agotado)".format(s.get_attribute("innerText"))
                            )
                        else:
                            sizes.append(s.get_attribute("innerText"))
                if not sizes:
                    sizes = ["Única"]
                allSizes.append(sizes)
                images = []
                self.driver.find_element_by_xpath(".//body").send_keys(Keys.END)
                while not images:
                    sleep(1)
                    for i in self.driver.find_elements_by_xpath(xpaths["images"]):
                        images.append(i.get_attribute("src"))
                allImages.append(images)
                self.driver.find_element_by_xpath(".//body").send_keys(Keys.HOME)
            if not colorsBtn:
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath(xpaths["sizesTags"])
                for s in sizesTags:
                    try:
                        s.find_element_by_xpath(xpaths["coming"])
                        sizes.append(
                            "{}(Próximamente)".format(s.get_attribute("innerText"))
                        )
                    except:
                        if "is-disabled" in s.get_attribute("class"):
                            sizes.append(
                                "{}(Agotado)".format(s.get_attribute("innerText"))
                            )
                        else:
                            sizes.append(s.get_attribute("innerText"))
                if not sizes:
                    sizes = ["Única"]
                allSizes.append(sizes)
                images = []
                self.driver.find_element_by_xpath(".//body").send_keys(Keys.END)
                if len(self.driver.find_elements_by_xpath(xpaths["images"])) < 2:
                    sleep(3)
                for i in self.driver.find_elements_by_xpath(xpaths["images"]):
                    images.append(i.get_attribute("src"))
                allImages.append(images)
                colors.append(images[0])
            self.db.add(
                Item(
                    self.brand,
                    name,
                    description,
                    priceBfr,
                    priceNow,
                    discount,
                    allImages,
                    url,
                    allSizes,
                    colors,
                    self.category,
                    self.originalCategory,
                    self.subcategory,
                    self.originalSubcategory,
                    self.sale,
                    self.gender,
                )
            )
        except Exception as e:
            print("Item saltado")
            print(e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


# Main Code
# ScrapBershka()