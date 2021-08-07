from Item import Item
from time import sleep
from Database import Database
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

brand = 'Stradivarius'
db = Database(brand)
xpaths={
    'categories':'.//div[@class="categories-menu "]//div[contains(@class,"menu-list-item")]/a',
    'categoriesSale':'.//ul[@class="product-categories"]/li/ul/li/a[span[contains(@style,"#f")]]',
    'colorsBtn':'.//div[@class="set-colors-product parent-center-child"]//img[@src]',
    'description':'.//span[@class="c-product-info--description-text"]',
    'discount':'.//div[@class="discount-percentage"]',
    'elems':'.//div[@class="product-grid-item item-generic-grid item-one-position-grid-2"]',
    'fast_priceBfr':'./div[@class="item-data-product"]/div/div/div/div/div[@class="one-old-price"]/div/span',
    'fast_priceNow':'./div[@class="item-data-product"]/div/div/div/div/div[@class="current-price"]/div/span',
    'fast_discount':'./div[@class="item-data-product"]/div/div/div/div/div[@class="discount-percentage"]',
    'href':'./div/a[@id="hrefRedirectProduct"]',
    'imgs':'.//div[@class="image-container"]/img',
    'main_categories':'.//div[contains(@class,"menu-list-item main-category ")]',
    'name':'.//h1[@class="product-name-title"]',
    'priceBfr':'.//div[@class="product-price block-height"]//div[@class="one-old-price"]//span',
    'priceNow':'.//div[@class="product-price block-height"]//div[@class="current-price"]//span',
    'priceNow2':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div/span',
    'sizesTags':'.//div[@id="productComponentRight"]//div[@class="size-grid-sizes-container"]//span',
    'subCats':'.//div[@class="display-inline-block child-center-parent slider-items-container"]/div/a',
    'subCats2':'.//div[@class="category-badges-list"]/a[not(text()="Ver todo")]'}

class ScrapStradivarius:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.set_page_load_timeout(30)
        self.driver.maximize_window()
        self.driver.get('https://www.stradivarius.com/co/')
        try:
            sleep(3)
            self.driver.find_element_by_xpath('.//button[@class="STRButton  cancel-button STRButton_secondary STRButton_large"]').click()
        except:
            print('No dismiss cookies')
        # try:
        #     self.driver.find_element_by_xpath('.//div[@class="burger-icon"]').click()
        #     sleep(2)
        # except:
        #     print('No menu open')
        # main_categories = self.driver.find_elements_by_xpath(xpaths['main_categories'])
        main_categories = self.driver.find_elements_by_xpath(xpaths['categories'])
        categories = [[],[]]
        # for i in range(len(main_categories)):
        #     i=main_categories[i]
        #     self.driver.execute_script('arguments[0].scrollIntoView();', i)
        #     if i.find_elements_by_xpath('./a[contains(@href,"javascript")]'):
        #         try:
        #             i.click()
        #             sleep(3)
        #             for c in self.driver.find_elements_by_xpath(xpaths['categories']):
        #                 if not c.get_attribute('href') in categories[1]:
        #                     categories[0].append(c.get_attribute('innerText'))
        #                     categories[1].append(c.get_attribute('href'))
        #         except:
        #             print('err')
        #     else:
        #         categories[0].append(i.text)
        #         categories[1].append(i.find_element_by_xpath('./a').get_attribute('href'))
        #     main_categories = self.driver.find_elements_by_xpath(xpaths['main_categories'])
        for c in main_categories:
            if not 'javascript:void' in c.get_attribute('href'):
                categories[0].append(c.get_attribute('innerText'))
                categories[1].append(c.get_attribute('href'))
        for c in range(len(categories[0])):
            self.category = categories[0][c]
            self.originalCategory = categories[0][c]
            self.subcategory = categories[0][c]
            self.originalSubcategory = categories[0][c]
            self.sale = False
            self.scrapCategory(categories[1][c])
        self.driver.quit()


    def scrapCategory(self, url):
        print(url)
        self.driver.get(url)
        sleep(1)
        subCats = [self.driver.find_elements_by_xpath(xpaths['subCats']),[]]
        if not subCats:
            sleep(1)
            subCats = [self.driver.find_elements_by_xpath(xpaths['subCats']),[]]
        if not subCats:
            sleep(5)
            subCats = [self.driver.find_elements_by_xpath(xpaths['subCats']),[]]
        for i in range(len(subCats[0])):
            subCats[1].append(subCats[0][i].find_element_by_xpath('./div[@class="name"]').text)
            subCats[0][i]=subCats[0][i].get_attribute('href')
        if subCats[0]:
            for i in range(len(subCats[0])):
                self.subcategory = subCats[1][i]
                self.originalSubcategory = subCats[1][i]
                self.scrapSubcategory(subCats[0][i])
        else:
            self.scrapSubcategory(url)

    def scrapSubcategory(self, url):
        self.driver.get(url)
        sleep(5)
        loading = True
        elems = self.driver.find_elements_by_xpath(xpaths['elems'])
        while loading:
            try:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(3)
                self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_UP)
                sleep(1)
                self.driver.find_element_by_xpath('.//body').send_keys(Keys.PAGE_UP)
                sleep(2)
                loading = len(elems) < len(self.driver.find_elements_by_xpath(xpaths['elems']))
                elems = self.driver.find_elements_by_xpath(xpaths['elems'])
            except:
                loading = False
        for elem in elems:
            self.driver.execute_script('arguments[0].scrollIntoView();', elem)
            href = elem.find_element_by_xpath(xpaths['href']).get_attribute('href')
            try:
                img = elem.find_element_by_xpath('.//img').get_attribute('src')
            except:
                img = ''
            if db.contains(href, img):
                db.update_product(elem, href, xpaths)
            else:
                self.scrapProduct(href)
            

    def scrapProduct(self, url):
        self.driver.execute_script('window.open("{}", "new window")'.format(url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            sleep(3)
            name = self.driver.find_elements_by_xpath(xpaths['name'])
            if not name:
                sleep(3)
                name = self.driver.find_elements_by_xpath(xpaths['name'])
            try:
                description = self.driver.find_element_by_xpath(xpaths['description']).text.capitalize()
            except:
                description = ' '
            priceNow = self.driver.find_element_by_xpath(xpaths['priceNow']).text
            try:
                priceBfr = self.driver.find_element_by_xpath(xpaths['priceBfr']).text
            except:
                priceBfr = priceNow
            try:
                discount = self.driver.find_element_by_xpath(xpaths['discount']).text
            except:
                discount = ' '
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
                    sizes.append(s.text)
                if len(sizesTags) == 0:
                    sizes = ["Única"]
                allSizes.append(sizes)
                images = []
                for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                    images.append(i.get_attribute("src"))
                allImages.append(images)
            if not allImages:
                images = []
                for i in self.driver.find_elements_by_xpath(xpaths['imgs']):
                    images.append(i.get_attribute("src"))
                allImages.append(images)
                sizes = []
                sizesTags = self.driver.find_elements_by_xpath(xpaths['sizesTags'])
                for s in sizesTags:
                    sizes.append(s.text)
                if len(sizesTags) == 0:
                    allSizes.append(["Única"])
            if name and allImages:
                name = name[0].text.capitalize()
                if not self.originalSubcategory:
                    self.originalSubcategory = ' '
                item = Item(brand,name,description,priceBfr,priceNow,discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale,"Mujer")
                db.add(item)
            else:
                print("Hubo un error")
        except Exception as e:
            print("Item saltado", url)
            print(e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


# Main Code
# ScrapStradivarius()
# mouse = webdriver.ActionChains(self.driver)
# mouse.move_to_element(self.driver.find_element_by_xpath('.//div[@class="child-center-parent sidebar-close col-xs-2"]')).click()
