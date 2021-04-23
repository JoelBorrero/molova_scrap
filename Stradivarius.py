from Item import Item
from time import sleep
from Database import Database
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

xpaths={
    'categories':'.//ul[@class="product-categories"]/li/ul/li/a[not(contains(@href,"rebajas")) and not(contains(@href,"novedades")) and not(span/span[contains(text(),"Ver todo")]) and not(span[contains(@style,"#f")])]',
    'categoriesSale':'.//ul[@class="product-categories"]/li/ul/li/a[span[contains(@style,"#f")]]',
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

class ScrapStradivarius:
    def __init__(self):
        options = Options()
        options.add_argument("user-data-dir=./Cookies/Stradivarius")
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome("./chromedriver.exe", options=options)
        self.driver.set_page_load_timeout(30)
        self.brand = "Stradivarius"
        self.db = Database(self.brand)
        self.driver.maximize_window()
        self.driver.get("https://www.stradivarius.com/co/")
        sleep(5)
        categories = [self.driver.find_elements_by_xpath('.//div[contains(@class,"category-content ")]/div/div/div[not(@class="sales-title")]'),[],[]]
        for c in categories[0]:
            cat = c.get_attribute("innerText").replace("\n", "")
            categories[1].append(c.find_element_by_xpath('./a').get_attribute("href"))
            try:
                c.find_element_by_xpath('./a[@style]')
                categories[2].append(True)
            except:
                categories[2].append(False)
            while cat.startswith(" "):
                cat = cat[1:]
            while cat.endswith(" "):
                cat = cat[:-1]
            categories[0][categories[0].index(c)] = cat
        for c in categories[0][2:]:
            if not any(s == c for s in ['Todos', 'Nuevo', 'Todos los Zapatos','NEW — Packs','NEW — Chalecos']):
                self.category = c
                self.originalCategory = c
                self.subcategory = c
                self.originalSubcategory = c
                self.sale = categories[2][categories[0].index(c)]
                self.scrapCategory(categories[1][categories[0].index(c)])
        self.driver.quit()
    def scrapCategory(self, url):
        self.driver.get(url)
        sleep(1)
        subCats = self.driver.find_elements_by_xpath('.//div[@class="display-inline-block child-center-parent slider-items-container"]/div/a')
        if len(subCats) > 0:
            for i in range(len(subCats)):
                if ("Ver todo" not in subCats[i].find_element_by_xpath('./div[@class="name"]').text):
                    self.subcategory = (subCats[i].find_element_by_xpath('./div[@class="name"]').text)
                    self.originalSubcategory = self.subcategory
                    self.scrapSubcategory(subCats[i].get_attribute("href"))
                    subCats = self.driver.find_elements_by_xpath('.//div[@class="display-inline-block child-center-parent slider-items-container"]/div/a')
        else:
            self.scrapSubcategory(url)

    def scrapSubcategory(self, url):
        self.driver.get(url)
        sleep(5)
        loading = True  # Testing
        elems = self.driver.find_elements_by_xpath('.//a[@id="hrefRedirectProduct"]')
        while loading:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            loading = len(elems) < len(self.driver.find_elements_by_xpath('.//a[@id="hrefRedirectProduct"]'))
            elems = self.driver.find_elements_by_xpath('.//a[@id="hrefRedirectProduct"]')
            self.driver.execute_script("arguments[0].scrollIntoView();", elems[-1])
        for e in elems:
            self.driver.execute_script("arguments[0].scrollIntoView();", e)
            self.scrapProduct(e.get_attribute("href"))

    def scrapProduct(self, url):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            sleep(3)
            name = self.driver.find_elements_by_xpath('.//h1[@class="product-name-title"]')
            if len(name) == 0:
                sleep(3)
                name = self.driver.find_elements_by_xpath('.//h1[@class="product-name-title"]')
            try:
                description = self.driver.find_element_by_xpath('.//div[@class="product-description text-transform-none"]').text.capitalize()
            except:
                description = ' '
            priceNow = self.driver.find_element_by_xpath('.//div[@class="current-price"]/div/span').text
            try:
                priceBfr = self.driver.find_element_by_xpath('.//div[@class="one-old-price"]/div/span').text
            except:
                priceBfr = priceNow
            try:
                discount = self.driver.find_element_by_xpath('.//div[@class="discount-percentage"]').get_attribute('innerText')
            except:
                discount = ' '
            colorsBtn = self.driver.find_elements_by_xpath('.//div[@class="set-colors-product parent-center-child"]/div[not(contains(@class,"display-none"))]/div/img')
            colors = []
            allSizes = []
            allImages = []
            for c in colorsBtn:
                c.click()
                colors.append(c.get_attribute("src"))
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath('.//div[@class="data-item-add-cart-favorite has-sizes "]/div/div[@class="size-grid-sizes-container"]/div/div[contains(@class,"item-grid-size")]')
                for s in sizesTags:
                    if "noStock" in s.get_attribute("class"):
                        sizes.append("{}(Agotado)".format(s.find_element_by_xpath("./span").get_attribute("innerText")))
                    else:
                        sizes.append(s.find_element_by_xpath("./span").get_attribute("innerText"))
                if len(sizesTags) == 0:
                    sizesTag = ["Única"]
                allSizes.append(sizes)
                images = []
                for i in self.driver.find_elements_by_xpath('.//div[@class="images-middle-container"]/div[@class="image-container"]/img'):
                    images.append(i.get_attribute("src"))
                allImages.append(images)
            if name:
                name = name[0].text.capitalize()
                if not self.originalSubcategory:
                    self.originalSubcategory = ' '
                self.db.add(Item(self.brand,name,description,priceBfr,priceNow,discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale,"Mujer"))
            else:
                print("Hubo un error")
        except Exception as e:
            print("Item saltado")
            print(e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


# Main Code
# ScrapStradivarius()
# mouse = webdriver.ActionChains(self.driver)
# mouse.move_to_element(self.driver.find_element_by_xpath('.//div[@class="child-center-parent sidebar-close col-xs-2"]')).click()