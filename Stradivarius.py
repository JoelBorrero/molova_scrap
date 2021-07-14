from Item import Item
from time import sleep
from Database import Database
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

xpaths={
    'categories':'.//ul[@class="product-categories"]/li/ul/li/a[not(contains(@href,"rebajas")) and not(contains(@href,"novedades")) and not(span/span[contains(text(),"Ver todo")]) and not(span[contains(@style,"#f")])]',
    'categoriesSale':'.//ul[@class="product-categories"]/li/ul/li/a[span[contains(@style,"#f")]]',
    'colorsBtn':'.//div[@class="c-product-info--header"]/div[contains(@class,"product-card-color-selector")]/div/div/div/img',
    'description':'.//span[@class="c-product-info--description-text"]',
    'discount':'./../..//div[@class="product-price--price product-price--price-discount"]',
    'elems':'.//div[@class="product-grid-item item-generic-grid item-one-position-grid-2"]',
    'fast_priceBfr':'./div[@class="item-data-product"]/div/div/div/div/div[@class="one-old-price"]/div/span',
    'fast_priceNow':'./div[@class="item-data-product"]/div/div/div/div/div[@class="current-price"]/div/span',
    'fast_discount':'./div[@class="item-data-product"]/div/div/div/div/div[@class="discount-percentage"]',
    'href':'./div/a[@id="hrefRedirectProduct"]',
    'imgs':'.//div[@id="product-grid"]/div/div/figure/img',
    'name':'.//h1[@class="title"]',
    'priceBfr':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div[@class="price price-old"]/span',
    'priceNow':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div[@class="sale"]/span',
    'priceNow2':'.//div[@class="c-product-info--header"]/div[@class="prices"]/div/span',
    'sizesTags':'.//div[@class="c-product-info--size"]/div/div/div[@class="product-card-size-selector--dropdown-sizes"]/div',
    'subCats':'.//div[@class="display-inline-block child-center-parent slider-items-container"]/div/a',
    'subCats2':'.//div[@class="category-badges-list"]/a[not(text()="Ver todo")]'}

class ScrapStradivarius:
    def __init__(self):
        options = Options()
        # options.add_argument("user-data-dir=./Cookies/Stradivarius")
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome("./chromedriver", options=options)
        self.driver.set_page_load_timeout(30)
        self.brand = "Stradivarius"
        self.db = Database(self.brand)
        self.driver.maximize_window()
        self.driver.get("https://www.stradivarius.com/co/")
        try:
            self.driver.find_element_by_xpath('.//button[@class="STRButton  cancel-button STRButton_secondary STRButton_large"]').click()
        except:
            print('No dismiss cookies')
        categories = [
            ['Todo a 35,900COP', 'Todo a 59,900COP', 'Todo a 69,900COP', 'Todo a 89,900COP', 'Favoritos Rebajas', 'Camisetas y buzos', 'Jeans', 'Pantalones', 'Vestidos', 'Camisas', 'Tops y Bodies', 'Faldas y Shorts', 'Chaquetas', 'Punto', 'Sport', 'Más accesorios', 'Bolsos y morrales', 'Bisutería', 'Correas', 'Home &amp; Living', 'Pijamas', 'Más accesorios', 'Todos los Zapatos', 'Sandalias', 'Tenis', 'Baletas', 'Tacones', 'Botas y botines', 'Nuevo', 'Ropa', 'Jeans', 'Vestidos', 'Camisetas', 'Camisas', 'Tops y Bodies', 'Shorts', 'Faldas', 'Pantalones', 'Monos y petos', 'Packs', 'Punto', 'Chaquetas', 'Conjuntos combinados', 'Pijamas', 'Buzos', 'Sport', 'Ver todo', 'Leggings', 'Partes de arriba', 'Partes de abajo', 'STR Teen', 'Ver todo', 'Shorts', 'Jeans', 'Pantalones', 'Camisetas', 'Punto', 'Vestidos', 'Calzado', 'Zapatos', 'Todos', 'Sandalias tacón', 'Sandalias planas', 'Sandalias plataforma', 'Tenis', 'Botas y botines', 'Accesorios', 'Ver todo', 'Bolsos y morrales', 'Bisutería', 'Más accesorios', 'Correas', 'Pijamas', 'Ver todo', 'Pijamas', 'Lencería', 'Calzado', 'Home &amp; Living', 'Ver todo', 'Decoración', 'Papelería', 'Fragancias'],
            ['https://www.stradivarius.com/co/mujer/rebajas/todo-a/todo-a-35%2C900cop-c1020297769.html', 'https://www.stradivarius.com/co/mujer/rebajas/todo-a/todo-a-59%2C900cop-c1020297768.html', 'https://www.stradivarius.com/co/mujer/rebajas/todo-a/todo-a-69%2C900cop-c1020275569.html', 'https://www.stradivarius.com/co/mujer/rebajas/todo-a/todo-a-89%2C900cop-c1020377270.html', 'https://www.stradivarius.com/co/mujer/rebajas/ropa/favoritos-rebajas-c1020329614.html', 'https://www.stradivarius.com/co/mujer/rebajas/ropa/camisetas-y-buzos/ver-todo-c1020330016.html', 'https://www.stradivarius.com/co/mujer/rebajas/ropa/jeans-c1390546.html', 'https://www.stradivarius.com/co/mujer/rebajas/ropa/pantalones-c1390549.html', 'https://www.stradivarius.com/co/mujer/rebajas/ropa/vestidos-c1020165026.html', 'https://www.stradivarius.com/co/mujer/rebajas/ropa/camisas-c1020040575.html', 'https://www.stradivarius.com/co/mujer/rebajas/ropa/tops-y-bodies/ver-todo-c1020172014.html', 'https://www.stradivarius.com/co/mujer/rebajas/ropa/faldas-y-shorts/ver-todo-c1020040596.html', 'https://www.stradivarius.com/co/mujer/rebajas/ropa/chaquetas/ver-todo-c1390544.html', 'https://www.stradivarius.com/co/mujer/rebajas/ropa/punto-c1020040574.html', 'https://www.stradivarius.com/co/mujer/rebajas/ropa/sport-c1020297767.html', 'https://www.stradivarius.com/co/mujer/rebajas/accesorios/m%C3%A1s-accesorios/all-accessoires-c1020377324.html', 'https://www.stradivarius.com/co/mujer/rebajas/accesorios/bolsos-y-morrales/ver-todo-c1020329514.html', 'https://www.stradivarius.com/co/mujer/rebajas/accesorios/bisuter%C3%ADa-c1020330019.html', 'https://www.stradivarius.com/co/mujer/rebajas/accesorios/correas-c1390528.html', 'https://www.stradivarius.com/co/mujer/rebajas/accesorios/home-%26-living/ver-todo-c1020273126.html', 'https://www.stradivarius.com/co/mujer/rebajas/accesorios/pijamas-c1020377536.html', 'https://www.stradivarius.com/co/mujer/rebajas/accesorios/m%C3%A1s-accesorios-c1020132603.html', 'https://www.stradivarius.com/co/mujer/rebajas/zapatos/todos-los-zapatos/todos-c1020273102.html', 'https://www.stradivarius.com/co/mujer/rebajas/zapatos/sandalias-c1020040559.html', 'https://www.stradivarius.com/co/mujer/rebajas/zapatos/tenis-c1399015.html', 'https://www.stradivarius.com/co/mujer/rebajas/zapatos/baletas-c1399016.html', 'https://www.stradivarius.com/co/mujer/rebajas/zapatos/tacones-c1399017.html', 'https://www.stradivarius.com/co/mujer/rebajas/zapatos/botas-y-botines-c1399011.html', 'https://www.stradivarius.com/co/mujer/nuevo-c1020093507.html', 'javascript:void(0)', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/jeans/ver-todo-c1718557.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/vestidos/ver-todo-c1020035501.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/camisetas/ver-todo-c1718528.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/camisas/ver-todo-c1718502.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/tops-y-bodies/ver-todo-c1020297562.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/shorts/ver-todo-c1020377546.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/faldas/ver-todo-c1718525.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/pantalones/ver-todo-c1718516.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/monos-y-petos-c1020371004.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/packs-c1020371005.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/punto/ver-todo-c1718564.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/chaquetas/ver-todo-c1020192003.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/conjuntos-combinados-c1020241016.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/pijamas-c1020371003.html', 'https://www.stradivarius.com/co/mujer/ropa/compra-por-producto/buzos-c1390587.html', 'javascript:void(0)', 'https://www.stradivarius.com/co/mujer/sport/compra-por-producto/ver-todo/ver-todo-c1020367540.html', 'https://www.stradivarius.com/co/mujer/sport/compra-por-producto/leggings/ver-todo-c1020367559.html', 'https://www.stradivarius.com/co/mujer/sport/compra-por-producto/partes-de-arriba-c1020367551.html', 'https://www.stradivarius.com/co/mujer/sport/compra-por-producto/partes-de-abajo/ver-todo-c1020367546.html', 'https://www.stradivarius.com/co/mujer/str-teen-c1020367562.html', 'https://www.stradivarius.com/co/mujer/str-teen/ver-todo-c1020367566.html', 'https://www.stradivarius.com/co/mujer/str-teen/shorts-c1020367570.html', 'https://www.stradivarius.com/co/mujer/str-teen/jeans-c1020367572.html', 'https://www.stradivarius.com/co/mujer/str-teen/pantalones-c1020367563.html', 'https://www.stradivarius.com/co/mujer/str-teen/camisetas-c1020367564.html', 'https://www.stradivarius.com/co/mujer/str-teen/punto-c1020367565.html', 'https://www.stradivarius.com/co/mujer/str-teen/vestidos-c1020367568.html', 'https://www.stradivarius.com/co/mujer/str-teen/calzado-c1020367571.html', 'javascript:void(0)', 'https://www.stradivarius.com/co/mujer/zapatos/compra-por-producto/todos/todos-c1020178528.html', 'https://www.stradivarius.com/co/mujer/zapatos/compra-por-producto/sandalias-tac%C3%B3n-c1399022.html', 'https://www.stradivarius.com/co/mujer/zapatos/compra-por-producto/sandalias-planas-c1399021.html', 'https://www.stradivarius.com/co/mujer/zapatos/compra-por-producto/sandalias-plataforma-c1399020.html', 'https://www.stradivarius.com/co/mujer/zapatos/compra-por-producto/tenis-c1399023.html', 'https://www.stradivarius.com/co/mujer/zapatos/compra-por-producto/botas-y-botines-c1399019.html', 'javascript:void(0)', 'https://www.stradivarius.com/co/mujer/accesorios/compra-por-producto/ver-todo/ver-todo-c1020303541.html', 'https://www.stradivarius.com/co/mujer/accesorios/compra-por-producto/bolsos-y-morrales/ver-todo-c1718540.html', 'https://www.stradivarius.com/co/mujer/accesorios/compra-por-producto/bisuter%C3%ADa/ver-todo-c1718569.html', 'https://www.stradivarius.com/co/mujer/accesorios/compra-por-producto/m%C3%A1s-accesorios/ver-todo-c1020303535.html', 'https://www.stradivarius.com/co/mujer/accesorios/compra-por-producto/correas-c1393011.html', 'https://www.stradivarius.com/co/mujer/pijamas-c1020367657.html', 'https://www.stradivarius.com/co/mujer/pijamas/ver-todo-c1020367659.html', 'https://www.stradivarius.com/co/mujer/pijamas/pijamas-c1020367658.html', 'https://www.stradivarius.com/co/mujer/pijamas/lencer%C3%ADa-c1020367660.html', 'https://www.stradivarius.com/co/mujer/pijamas/calzado-c1020367661.html', 'javascript:void(0)', 'https://www.stradivarius.com/co/mujer/home-%26-living/compra-por-producto/ver-todo/ver-todo-c1020367651.html', 'https://www.stradivarius.com/co/mujer/home-%26-living/compra-por-producto/decoraci%C3%B3n-c1020367623.html', 'https://www.stradivarius.com/co/mujer/home-%26-living/compra-por-producto/papeler%C3%ADa-c1020367598.html', 'https://www.stradivarius.com/co/mujer/home-%26-living/compra-por-producto/fragancias-c1020367631.html']]
        for c in range(len(categories[0])):
            self.category = categories[0][c]
            self.originalCategory = categories[0][c]
            self.subcategory = categories[0][c]
            self.originalSubcategory = categories[0][c]
            self.sale = False
            print(categories[0][c],categories[1][c])
            self.scrapCategory(categories[1][c])
        self.driver.quit()


    def scrapCategory(self, url):
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
        print(subCats)
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
        for e in elems:
            self.driver.execute_script('arguments[0].scrollIntoView();', e)
            href = e.find_element_by_xpath(xpaths['href']).get_attribute('href')
            if self.db.contains(href):
                self.updateProduct(e)
            else:
                self.scrapProduct(href)
            

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
                    sizes = ["Única"]
                allSizes.append(sizes)
                images = []
                for i in self.driver.find_elements_by_xpath('.//div[@class="images-middle-container"]/div[@class="image-container"]/img'):
                    images.append(i.get_attribute("src"))
                allImages.append(images)
            if name:
                name = name[0].text.capitalize()
                if not self.originalSubcategory:
                    self.originalSubcategory = ' '
                item=Item(self.brand,name,description,priceBfr,priceNow,discount,allImages,url,allSizes,colors,self.category,self.originalCategory,self.subcategory,self.originalSubcategory,self.sale,"Mujer")
                self.db.add(item)
            else:
                print("Hubo un error")
        except Exception as e:
            print("Item saltado")
            print(e)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def updateProduct(self, elem):
        url = elem.find_element_by_xpath(xpaths['href']).get_attribute('href')
        priceBfr = elem.find_element_by_xpath(xpaths['fast_priceBfr']).text
        priceNow = elem.find_element_by_xpath(xpaths['fast_priceNow']).text
        discount = elem.find_element_by_xpath(xpaths['fast_discount']).text
        self.db.update_product(url, priceBfr, priceNow, discount)


# Main Code
# ScrapStradivarius()
# mouse = webdriver.ActionChains(self.driver)
# mouse.move_to_element(self.driver.find_element_by_xpath('.//div[@class="child-center-parent sidebar-close col-xs-2"]')).click()
