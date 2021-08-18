import requests
from time import sleep
from random import uniform

from selenium import webdriver

from Item import Item
from Database import Database

brand = 'Mango'
db = Database(brand)
xpaths={
    'categories':'.//div[@class="section-detail-container section-detail-hidden "]/div/ul[@class="section-detail"]/li[not(contains(@class,"desktop-label-hidden") or contains(@class," label-hidden"))]/a',
    'discount':'.//span[@class="product-discount"]',
    'imgs':'.//div[@id="renderedImages"]//img',
    'name':'.//h1[@itemprop="name"]',
    'priceBfr':'.//span[contains(@class,"product-sale") and not(contains(@class,"discount"))]',
    'priceNow':'.//span[contains(@class,"product-sale")]'
}
endpoints = [
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.rebajas_she_mobile/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.SpecialSaleCO_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.nuevacoleccion_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.keytrends_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.accessoriesedition_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.essentials_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.best_sellers_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?idSubSection=vestidos_she&menu=familia;32,34,432,460&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?menu=familia;14,414&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?menu=familia;18,318,320,46,418&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?menu=familia;55,355,810,455,611&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?idSubSection=sudaderas_she&menu=familia;610&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?idSubSection=chaquetas_she&menu=familia;16,304,404&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?menu=familia;15,402&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?menu=familia;26,326,22,322,426&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?menu=familia;28,428&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?menu=familia;20,420&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?menu=familia;25,422&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?menu=familia;88,68&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?idSubSection=bodies_she&menu=familia;38,438&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.prendas_she/?idSubSection=pijamas_she&menu=familia;628&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.accesorios_she/?idSubSection=zapatos_she&menu=accesorio;42,342,442&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.accesorios_she/?idSubSection=bolsos_she&menu=accesorio;40,340,440&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.accesorios_she/?idSubSection=bisuteria_she&menu=accesorio;48,448&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.accesorios_she/?idSubSection=marroquineria_she&menu=accesorio;56,620&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.accesorios_she/?idSubSection=cinturones_she&menu=accesorio;44,444&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.accesorios_she/?idSubSection=gafas_she&menu=accesorio;50,777&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.accesorios_she/?idSubSection=bufandasypanuelos_she&menu=accesorio;53,452&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.accesorios_she/?idSubSection=gorrosyguantes_she&menu=accesorio;49,45&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.accesorios_she/?idSubSection=masaccesorios_she&menu=accesorio;41,58,59,457,436,57&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.accesorios_she/?idSubSection=mascarillasygeles_she&menu=accesorio;800,801,805&saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.weddings/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.Bano2021_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.ActiveWear_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.lino_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.comfycollection/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.TotalLook_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.ExclusivoOnline_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.denim_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.office_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.maternity_she/?saleSeasons=3,8,5,4&pageNum=',
    'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale.violeta/?saleSeasons=3,8,5,4&pageNum='
    ]

class ScrapMango:
    def __init__(self):
        self.scrap()
        self.crawl_api()

    def scrap(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.set_page_load_timeout(30)
        self.driver.maximize_window()
        self.driver.get('https://shop.mango.com/co/mujer')
        self.driver.find_element_by_id('onetrust-accept-btn-handler').click()
        endpoints = []
        categories = []
        for i in self.driver.find_elements_by_xpath(xpaths['categories']):
            categories.append(i.get_attribute('href'))
        for category in categories:
            self.driver.get(category)
            scriptToExecute = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;'
            netData = self.driver.execute_script(scriptToExecute)
            for i in netData:
                if '/services/productlist/products/CO/she/' in i['name']:
                    endpoint = (i['name'])
                    endpoint = endpoint[:endpoint.index('&pageNum=')+9]
                    if not endpoint in endpoints:
                        endpoints.append(endpoint)
        self.driver.quit()

    def crawl_api(self):
        open('./Database/Mango.json', 'w').close()
        for endpoint in endpoints:
            pageNum = 1
            print(endpoint)
            while pageNum != 0:
                response = requests.get(endpoint+str(pageNum)).json()
                self.category = response['titleh1']
                garments = response['groups'][0]['garments']
                for item in garments:
                    it = garments[item]
                    allImages = []
                    allSizes = []
                    colors = []
                    for color in it['colors']:
                        images = []
                        sizes = []
                        for image in color['images']:
                            images.append(image['img1Src'])
                        for size in color['sizes']:
                            sizes.append(size['label']+('(Agotado)' if size['stock'] == 0 else ''))
                        allImages.append(images)
                        allSizes.append(sizes)
                        colors.append(color['iconUrl'].replace(' ',''))
                    allImages.reverse()#I don't know why
                    db.add(
                        Item(
                            brand,
                            it['shortDescription'],
                            it['shortDescription'],
                            it['price']['crossedOutPrices'],
                            [it['price']['salePrice']],
                            it['price']['discountRate'],
                            allImages,
                            'https://shop.mango.com'+it['colors'][0]['linkAnchor'],
                            allSizes,
                            colors,
                            self.category,
                            self.category,
                            self.category,
                            self.category,
                            False,
                            "Mujer"))
                print('Page',pageNum,len(garments))
                if len(garments)<300:
                    pageNum = 0
                else:
                    pageNum += 1
                sleep(uniform(5,10))
        db.close()


# ScrapMango()