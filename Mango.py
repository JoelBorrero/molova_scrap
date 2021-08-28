import requests
import ast
from time import sleep
from random import uniform
from datetime import datetime
import pytz

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
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.nuevacoleccion_she/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.nuevo/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.keytrends_she/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.accessoriesedition_she/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.prendas_she/?idSubSection=vestidos_she&menu=familia;32,34,432,460&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.prendas_she/?idSubSection=camisas_she&menu=familia;14,414&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.prendas_she/?idSubSection=camisetas_she&menu=familia;18,318,320,46,418&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.prendas_she/?idSubSection=cardigans_she&menu=familia;55,355,810,455&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.prendas_she/?idSubSection=sudaderas_she&menu=familia;610,611&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.prendas_she/?idSubSection=chaquetas_she&menu=familia;16,304,404&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.prendas_she/?idSubSection=pantalones_she&menu=familia;26,326,22,322,426&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.prendas_she/?idSubSection=bodies_she&menu=familia;38,438&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.prendas_she/?idSubSection=pijamas_she&menu=familia;628&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.accesorios_she/?idSubSection=zapatos_she&menu=accesorio;42,342,442&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.accesorios_she/?idSubSection=bolsos_she&menu=accesorio;40,340,440&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.accesorios_she/?idSubSection=bisuteria_she&menu=accesorio;48,448&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.accesorios_she/?idSubSection=marroquineria_she&menu=accesorio;56,620&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.accesorios_she/?idSubSection=cinturones_she&menu=accesorio;44,444&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.accesorios_she/?idSubSection=gafas_she&menu=accesorio;50,777&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.accesorios_she/?idSubSection=bufandasypanuelos_she&menu=accesorio;53,452&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.accesorios_she/?idSubSection=gorrosyguantes_she&menu=accesorio;49,45&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.accesorios_she/?idSubSection=masaccesorios_she&menu=accesorio;41,58,59,457,436,57&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.accesorios_she/?idSubSection=mascarillasygeles_she&menu=accesorio;800,801,805&saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.weddings/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.Bano2021_she/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.ActiveWear_she/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.lino_she/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.comfycollection_she/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.TotalLook_she/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.ExclusivoOnline_she/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.denim_she/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.office_she/?saleSeasons=4,8,5,3&pageNum=',
                'https://shop.mango.com/services/productlist/products/CO/she/sections_she_colombia_rebajas_SpecialSale_HighViz_ClickDeals.maternity_she/?saleSeasons=4,8,5,3&pageNum='
            ]

class ScrapMango:
    def __init__(self):
        if not endpoints:
            self.scrap()
        APICrawler()

def scrap_for_links():
    driver = webdriver.Chrome('./chromedriver')
    driver.set_page_load_timeout(30)
    driver.maximize_window()
    driver.get('https://shop.mango.com/co/mujer')
    sleep(2)
    try:
        driver.find_element_by_id('onetrust-accept-btn-handler').click()
        driver.find_element_by_xpath('.//div[@class="icon closeModal icon__close desktop confirmacionPais"]').click()
    except:
        print('Something not dismissed')
    endpoints.clear()
    categories = []
    for i in driver.find_elements_by_xpath(xpaths['categories']):
        categories.append(i.get_attribute('href'))
    for category in categories:
        driver.get(category)
        scriptToExecute = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;'
        netData = driver.execute_script(scriptToExecute)
        for i in netData:
            if '/services/productlist/products/CO/she/' in i['name']:
                endpoint = (i['name'])
                endpoint = endpoint[:endpoint.index('&pageNum=')]
                if not endpoint in endpoints:
                    endpoints.append((category, endpoint))
    driver.quit()
    settings = ast.literal_eval(open('./Settings.txt','r').read())
    settings[brand]['endpoints']=endpoints
    with open('./Settings.txt','w') as s:
        s.write(str(settings))

class APICrawler:
    def __init__(self, endpoints):
        open('./Database/Mango.json', 'w').close()
        open('./Database/LogsMNG.txt','w').close()
        tz = pytz.timezone('America/Bogota')
        for endpoint in endpoints:
            logs = open('./Database/LogsMNG.txt','a')
            logs.write(f'{datetime.now(tz).hour}:{datetime.now(tz).minute}   -   {endpoint[0]}\n')
            pageNum = 1
            while pageNum != 0:
                response = requests.get(endpoint[1]+str(pageNum)).json()
                self.category = response['titleh1']
                garments = response['groups'][0]['garments']
                logs.write(f'    {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {len(garments)} products. (Page {pageNum})\n')
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
                            it['garmentId'],
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
                    logs.write(f'      + {datetime.now(tz).hour}:{datetime.now(tz).minute}:{datetime.now(tz).second}   -   {it["shortDescription"]}\n')
                if len(garments) < 300 or pageNum > 4:
                    pageNum = 0
                else:
                    pageNum += 1
                sleep(uniform(30,120))
            logs.close()
        db.close()


# ScrapMango()