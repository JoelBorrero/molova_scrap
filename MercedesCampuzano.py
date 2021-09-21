from Item import Item
from time import sleep
from Database import Database
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

brand = "Mercedes Campuzano"
db = Database(brand)
xpaths = {
    'categories': './/ul[@class="vtex-menu-2-x-menuContainer list flex pl0 mv0 flex-row"]/div/div/div/div/div/li/div',
    'closeBtn': './/button[@class="vtex-modal-layout-0-x-closeButton vtex-modal-layout-0-x-closeButton--modal-header ma0 bg-transparent pointer bw0 pa3"]',
    'color': './/img[@class="vtex-store-components-3-x-skuSelectorItemImageValue mercedescampuzano-mcampuzano-1-x-showImgColor"]',
    'colorsBtn': './/ul[@class="vtex-slider-0-x-sliderFrame list pa0 h-100 ma0 flex justify-center"]/li[not(.//button)]',
    'description': './/div[@class="vtex-store-components-3-x-specificationsTableContainer mt9 mt0-l pl8-l"]',
    'description2': './/div[@class="vtex-store-components-3-x-content vtex-store-components-3-x-content--product-description h-auto"]',
    'discount': './/div[@class="vtex-store-components-3-x-discountInsideContainer t-mini white absolute right-0 pv2 ph3 bg-emphasis z-1"]',
    'elems': './/section[@class="vtex-product-summary-2-x-container vtex-product-summary-2-x-containerNormal overflow-hidden br3 h-100 w-100 flex flex-column justify-between center tc"]',
    'href': "./a",
    'fast_discount': './a//div[contains(@class,"discountInsideContainer")]',
    'fast_priceBfr': './a//div/span[contains(@class,"strike")]/span',
    'fast_priceNow': './a//div/span[@class="vtex-store-components-3-x-sellingPrice vtex-store-components-3-x-sellingPriceValue vtex-product-summary-2-x-sellingPrice vtex-product-summary-2-x-sellingPrice--sosPrice dib ph2 t-body t-heading-5-ns vtex-product-summary-2-x-price_sellingPrice vtex-product-summary-2-x-price_sellingPrice--sosPrice"]/span',
    'imgs': './/div[contains(@class,"swiper-slide vtex-store-components-3-x-productImagesGallerySlide center-all")]/div/div/div/img',
    'name': './/span[@class="vtex-store-components-3-x-productBrand "]',
    'name2': './/span[contains(@class,"vtex-store-components-3-x-currencyInteger vtex-store-components-3-x-currencyInteger--price"]',
    'priceBfr': './/div[contains(@class,"priceContainer")]/div/span',
    'priceNow': './/span[contains(@class,"vtex-store-components-3-x-price_sellingPrice--price")]',
    'prices': './/span[@class="vtex-store-components-3-x-currencyContainer vtex-store-components-3-x-currencyContainer--price"]',
    'ref': '',
    'saleCategory': './/a[@class="vtex-breadcrumb-1-x-link vtex-breadcrumb-1-x-link--1 dib pv1 link ph2 c-muted-2 hover-c-link"]',
    'subCats': './/div[contains(@class,"vtex-menu-2-x-submenuContainer ")]/div/section/nav/ul/li/div/a',
    'subCats2': './/a[@class="vtex-slider-layout-0-x-imageElementLink vtex-slider-layout-0-x-imageElementLink--menu-slider vtex-store-components-3-x-imageElementLink vtex-store-components-3-x-imageElementLink--menu-slider"]',
}


class ScrapMercedesCampuzano:
    def __init__(self):
        # self.driver = webdriver.Chrome("./chromedriver.exe")
        self.driver = webdriver.Chrome("./chromedriver")
        self.driver.set_page_load_timeout(30)
        self.driver.maximize_window()
        self.gender = "Mujer"
        self.sale = False
        mouse = webdriver.ActionChains(self.driver)
        self.driver.get("https://www.mercedescampuzano.com/")
        for i in range(5):
            try:
                self.driver.find_element_by_xpath(xpaths["closeBtn"]).click()
                break
            except:
                sleep(2)
        subCats = []
        categories = self.driver.find_elements_by_xpath(xpaths["categories"])
        for c in categories:
            mouse.move_to_element(c).perform()
            for s in self.driver.find_elements_by_xpath(xpaths["subCats"]):
                try:
                    subCats.append(s.get_attribute("href"))
                except:
                    pass
            if not self.driver.find_elements_by_xpath(xpaths["subCats"]):
                for s in self.driver.find_elements_by_xpath(
                        xpaths["subCats2"]):
                    subCats.append(s.get_attribute("href"))
        for c in subCats:
            self.category = c
            self.subcategory = self.category
            self.originalCategory = self.category
            self.originalSubcategory = self.category
            self.scrapCategory(c)
        self.driver.quit()

    def scrapCategory(self, url):
        self.driver.get(url)
        sleep(5)
        if self.sale:
            self.category = self.driver.find_element_by_xpath(xpaths["saleCategory"]).text
            self.subcategory = self.category
            self.originalCategory = self.category
            self.originalSubcategory = self.category
        loading = True
        elems = self.driver.find_elements_by_xpath(xpaths["elems"])
        while loading:
            try:
                self.driver.find_element_by_xpath(".//body").send_keys(
                    Keys.END)
                sleep(3)
                self.driver.find_element_by_xpath(".//body").send_keys(
                    Keys.PAGE_UP)
                sleep(1)
                self.driver.find_element_by_xpath(".//body").send_keys(
                    Keys.PAGE_UP)
                sleep(2)
                if len(elems) == len(
                        self.driver.find_elements_by_xpath(xpaths["elems"])):
                    sleep(3)
                loading = len(elems) < len(
                    self.driver.find_elements_by_xpath(xpaths["elems"]))
                elems = self.driver.find_elements_by_xpath(xpaths["elems"])
            except:
                loading = False
        for elem in elems:
            self.driver.execute_script("arguments[0].scrollIntoView();", elem)
            url = elem.find_element_by_xpath(
                xpaths["href"]).get_attribute("href")
            if db.contains(url):
                db.update_product(elem, url, xpaths)
            else:
                self.scrapProduct(url)

    def scrapProduct(self, url):
        try:
            self.driver.execute_script(
                'window.open("{}", "new window")'.format(url))
            self.driver.switch_to.window(self.driver.window_handles[1])
            try:
                priceNow = self.driver.find_elements_by_xpath(
                    xpaths["prices"])[1].text  # 16/03/21
                priceBfr = self.driver.find_elements_by_xpath(
                    xpaths["prices"])[0].text
                discount = self.driver.find_element_by_xpath(
                    xpaths["discount"]).text
            except:
                try:
                    priceNow = self.driver.find_elements_by_xpath(
                        xpaths["prices"])[0].text  # 16/03/21
                except:
                    try:
                        priceNow = self.driver.find_element_by_xpath(
                            xpaths["priceNow"]).text
                    except:
                        sleep(3)
                        priceNow = self.driver.find_element_by_xpath(
                            xpaths["priceNow"]).text
                priceBfr = priceNow
                discount = " "
            ref = 'ref'
            try:
                description = self.driver.find_element_by_xpath(
                    xpaths["description"]).get_attribute("innerText")
            except:
                description = self.driver.find_element_by_xpath(
                    xpaths["description2"]).get_attribute("innerText")
            colorsBtn = self.driver.find_elements_by_xpath(xpaths["colorsBtn"])
            colors = []
            allSizes = []
            comunName = []
            skipName = [[], []]
            allImages = []
            # self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_DOWN)
            for c in range(len(colorsBtn) + 1):
                try:
                    name = self.driver.find_element_by_xpath(
                        xpaths["name"]).text
                except:
                    name = self.driver.find_element_by_xpath(
                        xpaths["name2"]).text
                if not comunName:
                    comunName = name.split(" ")
                else:
                    for j in comunName:
                        if not j in name:
                            comunName.remove(j)
                w = name.split(" ")[0]
                if w in skipName[0]:
                    skipName[1][skipName[0].index(w)] = (
                        skipName[1][skipName[0].index(w)] + 1)
                else:
                    skipName[0].append(w)
                    skipName[1].append(1)
                colorsBtn = self.driver.find_elements_by_xpath(
                    xpaths["colorsBtn"])
                colorsBtn.insert(0, "init")
                if c > 0:
                    colorsBtn[c].click()
                try:
                    colors.append(
                        self.driver.find_element_by_xpath(
                            xpaths["color"]).get_attribute("src"))
                except:
                    sleep(3)
                    try:
                        colors.append(
                            self.driver.find_element_by_xpath(
                                xpaths["color"]).get_attribute("src"))
                    except:
                        sleep(2)
                        try:
                            colors.append(
                                self.driver.find_element_by_xpath(
                                    xpaths["color"]).get_attribute("src"))
                        except:
                            colors.append(
                                self.driver.find_element_by_xpath(
                                    xpaths["imgs"]).get_attribute("src"))
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath(
                    './/div[contains(@class,"flex flex-column vtex-store-components-3-x-skuSelectorSubcontainer--talla mb3 vtex-store-components-3-x-skuSelectorSubcontainer")]/div/div[@class="vtex-store-components-3-x-skuSelectorOptionsList w-100 inline-flex flex-wrap ml2 items-center"]/div'
                )
                for s in sizesTags:
                    if s.find_elements_by_xpath(
                            './div/div[@class="absolute absolute--fill vtex-store-components-3-x-diagonalCross"]'
                    ):
                        sizes.append("{}(Agotado)".format(
                            s.get_attribute("innerText")))
                    else:
                        sizes.append(s.get_attribute("innerText"))
                if not sizes:
                    sizes = ["Única"]
                allSizes.append(sizes)
                images = []
                imgs = self.driver.find_elements_by_xpath(xpaths["imgs"])
                while not imgs:
                    sleep(1)
                    imgs = self.driver.find_elements_by_xpath(xpaths["imgs"])
                for i in imgs:
                    images.append(i.get_attribute("src"))
                allImages.append(images)
            name = " ".join(comunName)
            w = skipName[0][skipName[1].index(max(skipName[1]))]
            if not name.startswith(w):
                name = " ".join([w, name])
            db.add(
                Item(
                    brand,
                    name,
                    ref,
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
                ))
        except Exception as e:
            print("Item saltado", url)
            print(e)
            # inst = input('Continuar...')
            # while inst != '':
            #    try:
            #        exec(print(inst))
            #    except:
            #        print('err')
            #    inst = input('...')
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


# Main Code
# ScrapMercedesCampuzano()
