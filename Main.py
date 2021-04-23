import os, boto3, time, json, scrapy, Bershka, Gef, MercedesCampuzano, PullAndBear, Stradivarius, Zara

from scrapy.crawler import CrawlerProcess

from Private import private
from Item import Item, toPrice
from Database import Database


def is_valid_json(path):
    try:
        with open(path, "r", encoding="utf8") as f:
            j = json.loads(f.read())
        return True
    except:
        return False

def upload(lastLoad, uploadAll=False):
    if uploadAll:
        lastLoad = time.time()
    access_key = private["access_key"]
    secret_access_key = private["secret_access_key"]
    bucket = "recursosmolova"
    client = boto3.client(
        "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_access_key
    )
    path = "C://Users/JoelBook/Documents/Molova/Items"
    for file in os.listdir(path):
        if ".json" in file:
            name = "Items/{}".format(str(file))
            if os.path.getmtime("{}/{}".format(path, file)) > lastLoad or uploadAll:
                if is_valid_json("{}/{}".format(path, file)):
                    client.upload_file("{}/{}".format(path, file), bucket, name)
                    print("Uploading", file)
                else:
                    print(file, "parece estar dañado")
    return time.time()

def merge():
    error = 0
    totalItems = 0
    percentage = 0
    index = 0
    bar = ""
    path = "C:/Users/JoelBook/Documents/Molova/Items"
    files = os.listdir(path)
    for file in files:
        if ".json" in file:
            old = file
            file = f"remove{files.index(file)}.json"
            os.rename(f"{path}/{old}", f"{path}/{file}")
            with open("{}/{}".format(path, file), "r", encoding="utf8") as f:
                j = json.loads(f.read())
                try:
                    for c in j["categories"]:
                        totalItems += len(c["items"])
                except:
                    os.remove(f"{path}/{file}")
    for file in os.listdir(path):
        if ".json" in file:
            with open("{}/{}".format(path, file), "r", encoding="utf8") as f:
                j = json.loads(f.read())
                try:
                    for c in j["categories"]:
                        for i in c["items"]:
                            # Item.Item(i['brand'],i['name'],i['description'],i['priceBefore'],i['allPricesNow'],i['discount'],i['allImages'],i['url'],i['allSizes'],i['colors'],i['category'],i['originalCategory'],i['subcategory'],i['originalSubcategory'],i['sale'],i['gender'])
                            index += 1
                            if not percentage == int(index / totalItems * 100):
                                percentage = int(index / totalItems * 100)
                                bar = "{}°".format(bar)
                                print(
                                    "{}% ({} de {}) {}".format(
                                        percentage, index, totalItems, bar
                                    )
                                )
                except:
                    error += 1
    print(error)
    input("\nPresione enter para salir\n")

def scrap():
    brands = [
        # "Zara",
        #"MercedesCampuzano",
        # "Bershka",
        "Stradivarius",
        "PullAndBear",
        "Gef",
        ]
    lastLoad = time.time()
    for brand in brands:
        s=time.localtime(time.time())
        with open("Items/Log.txt","a",encoding="utf8") as f:
            f.write(f"Inicia {brand}: {s.tm_hour}:{s.tm_min}\n")
        try:
            exec("{0}.Scrap{0}()".format(brand))
        except:
            print("Error scrapping", brand)
        lastLoad = upload(lastLoad)
        s=time.localtime(time.time())
        with open("Items/Log.txt","a",encoding="utf8") as f:
            f.write(f"Acaba {brand}: {s.tm_hour}:{s.tm_min}\n\n")

urlsDb = Database('Urls')
bDb = Database('Bershka')
gDb = Database('Gef')
mDb = Database('Mercedes Campuzano')
zDb = Database('Zara')
pDb = Database('Pull & Bear')

class ItemsSpider(scrapy.Spider):
    name = "Items"
    #user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
    start_urls = urlsDb.getAllUrls()
    #custom_settings = {}
    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
        "Sec-Fetch-User": "?1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",}
    firstUrl = urlsDb.firstUrl()
    #params = {}
    #def start_requests(self):
    #    yield scrapy.Request(self.firstUrl, headers=self.headers, callback = self.parse)

    def parse(self, response):
        def dataFromZaraJson(json):
            item = {}
            item['description'] = json['description']
            output = []
            for color in json["colors"]:
                data = {}
                data["name"] = color["name"]
                sizes = []
                imgs = []
                for s in color["sizes"]:
                    a = "" if s["availability"] == "in_stock" else "(Agotado)"
                    sizes.append(f'{s["name"]}{a}')
                for img in color["mainImgs"]:
                    imgs.append(
                        f'https://static.zara.net/photos//{img["path"]}/w/496/{img["name"]}.jpg'
                    )
                data["sizes"] = sizes
                data["imgs"] = imgs
                output.append(data)
            item['colors']=output
            return item
        xpaths = {
            'Bershka':{
                'category'      : '',
                'color'         : './/ul[@class="swiper-wrapper"]/li/a/div/img/@scr',
                'description'   : './/section[@class="product-info"]/text()',
                'discount'      : './/span[@class="discount-tag"]/text()',
                'imgs'          : './/div/button/div[@class="image-item-wrapper"]/img/@src',
                'name'          : './/h1[@class="product-title"]/text()',
                'priceBefore'   : './/span[@class="old-price-elem"]/text()',
                'priceBefore2'  : './/span[@class="old-price-elem"]/text()',
                'priceNow'      : './/div[contains(@class,"current-price-elem")]/text()',
                'sizes'         : './/div[@class="sizes-list-detail"]/ul/li/button',
                'stock'         : '',
                'subCat'        : '',
                'hasStock'      : '',},
            'Gef':{
                'category'      : '',
                'color'         : '',
                'description'   : '',
                'discount'      : '',
                'imgs'          : '',
                'name'          : '',
                'priceBefore'   : '',
                'priceBefore2'  : '',
                'priceNow'      : '',
                'sizes'         : '',
                'stock'         : '',
                'subCat'        : '',
                'hasStock'      : '',},
            'Mercedes Campuzano':{
                'category'      : './/a[@class="vtex-breadcrumb-1-x-link vtex-breadcrumb-1-x-link--1 dib pv1 link ph2 c-muted-2 hover-c-link"]/text()',
                'color'         : './/img[@class="vtex-store-components-3-x-skuSelectorItemImageValue mercedescampuzano-mcampuzano-1-x-showImgColor"]/@src',
                'colorsBtn'     : './/ul[@class="vtex-slider-0-x-sliderFrame list pa0 h-100 ma0 flex justify-center"]/li[not(.//button)]',
                'description'   : './/div[@class="vtex-store-components-3-x-content vtex-store-components-3-x-content--product-description h-auto"]//text()',
                'description2'  : './/div[@class="vtex-store-components-3-x-specificationsTableContainer mt9 mt0-l pl8-l"]',
                'discount'      : './/div[@class="vtex-store-components-3-x-discountInsideContainer t-mini white absolute right-0 pv2 ph3 bg-emphasis z-1"]//text()',
                'hasStock'      : 'absolute absolute--fill vtex-store-components-3-x-diagonalCross',
                'imgs'          : './/div[contains(@class,"swiper-slide vtex-store-components-3-x-productImagesGallerySlide center-all")]/div/div/div/img/@src',
                'name'          : './/span[@class="vtex-store-components-3-x-productBrand "]/text()',
                'name2'         : './/span[contains(@class,"vtex-store-components-3-x-currencyInteger vtex-store-components-3-x-currencyInteger--price"]',
                'priceBefore'   : './/div[@class="vtex-store-components-3-x-listPrice t-small-s t-small-ns c-muted-2 mb2 vtex-store-components-3-x-price_listPriceContainer vtex-store-components-3-x-price_listPriceContainer--price"]//text()',
                'priceBefore2'  : './/div[@class="vtex-store-components-3-x-listPrice t-small-s t-small-ns c-muted-2 mb2 vtex-store-components-3-x-price_listPriceContainer vtex-store-components-3-x-price_listPriceContainer--price"]//text()',
                'priceNow'      : './/div[@class="vtex-store-components-3-x-sellingPrice vtex-store-components-3-x-sellingPriceContainer pv1 b c-on-base vtex-store-components-3-x-price_sellingPriceContainer vtex-store-components-3-x-price_sellingPriceContainer--price"]//text()',
                'sizes'         : './/div[@class="vtex-store-components-3-x-valueWrapper vtex-store-components-3-x-skuSelectorItemTextValue c-on-base center pl5 pr5 z-1 t-body"]/text()',
                'stock'         : './/div[@class="vtex-store-components-3-x-skuSelectorInternalBox w-100 h-100 b--muted-4 br2 b z-1 c-muted-5 flex items-center overflow-hidden hover-b--muted-2 ba" and div[@class="vtex-store-components-3-x-valueWrapper vtex-store-components-3-x-skuSelectorItemTextValue c-on-base center pl5 pr5 z-1 t-body"]]/*[1]/@class',
                'subCat'        : './/a[@class="vtex-breadcrumb-1-x-link vtex-breadcrumb-1-x-link--2 dib pv1 link ph2 c-muted-2 hover-c-link"]/text()',
                },
            'Pull & Bear':{
                'category'      : '',
                'color'         : '',
                'description'   : '',
                'discount'      : '',
                'imgs'          : '',
                'name'          : '',
                'priceBefore'   : '',
                'priceBefore2'  : '',
                'priceNow'      : '',
                'sizes'         : '',
                'stock'         : '',
                'subCat'        : '',
                'hasStock'      : '',
                },
            'Zara':{
                'category'      : './/div[@class="expandable-text__inner-content"]/p/text()',
                'color'         : './/p[contains(@class,"product-detail-info__color")]',
                'description'   : './/div[@class="expandable-text__inner-content"]/p/text()',
                'discount'      : './/div[@class="product-detail-info__price-amount price"]/span/span/text()',
                'imgs'          : './/div[@class="media__wrapper media__wrapper--fill media__wrapper--force-height"]/picture/img[@class="media-image__image media__wrapper--media"]/@src',
                'name'          : './/h1[contains(@class,"info__name")]/text()',
                'priceBefore'   : './/div[@class="product-detail-info__price-amount price"]/span[@class="price__amount price__amount--old"]/text()',
                'priceNow'      : './/span[@class="price__amount"]/text()',
                'sizes'         : './/span[contains(@class,"product-size-info__main-label")]/text()',
                'stock'         : './/ul[contains(@id,"product-size-selector-product-detail-info-")]/li/@class',
                'subCat'        : './/div[@class="expandable-text__inner-content"]/p/text()',
                'hasStock'      : 'item--is-disabled',}
        }
        if 'bershka' in response.url:
            brand = 'Bershka'
            db = bDb
        elif 'gef' in response.url:
            brand = 'Gef'
            db = gDb
        elif 'mercedes' in response.url:
            brand = 'Mercedes Campuzano'
            db = mDb
        elif 'zara' in response.url:
            brand = 'Zara'
            db = zDb
        elif all(w in response.url for w in ['pull','bear']):
            brand = 'Zara'
            db = pDb
        else:
            brand = 'Brand'
            print('ERROR>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',response.url)
            db = Database('Brand')
        gender = 'Hombre' if 'hombre' in response.url else 'Mujer'
        temp = [response.xpath(xpaths[brand]['sizes']).getall(),response.xpath(xpaths[brand]['stock']).getall()]
        sizes = []
        for i in range(len(temp[0])):
            if xpaths[brand]['hasStock'] in temp[1][i]:
                sizes.append('{}(Agotado)'.format(temp[0][i]))
            else:
                sizes.append(temp[0][i])
        # temp.clear()
        priceNow = toPrice(response.xpath(xpaths[brand]['priceNow']).get())
        priceBefore = toPrice(response.xpath(xpaths[brand]['priceBefore']).getall())
        if priceBefore == '$ 0':
            priceBefore = priceNow
        jsonData = response.xpath('.//body/script/text()').get()
        jsonData = jsonData[jsonData.index('window.zara.viewPayload')+26 : -1]
        jsonData = json.loads(jsonData)
        jsonData = jsonData['product']
        name = response.xpath(xpaths[brand]['name']).get()
        description = response.xpath(xpaths[brand]['description']).get()
        if not name:
            name = jsonData['name']
        jsonData = jsonData['detail']
        imgs = []
        colors = []
        sizes = []
        jsonData = dataFromZaraJson(jsonData)
        if not description:
            description = jsonData['description']
        for color in jsonData['colors']:
            colors.append(color['name'])
            imgs.append(color['imgs'])
            sizes.append(color['sizes'])
        item=Item(
            brand,
            name,
            description,
            priceBefore,
            priceNow,
            ''.join(response.xpath(xpaths[brand]['discount']).getall()).replace('\xa0',''),
            imgs,
            response.url,
            sizes,
            colors,
            response.xpath(xpaths[brand]['category']).get(),
            response.xpath(xpaths[brand]['category']).get(),
            response.xpath(xpaths[brand]['subCat']).get(),
            response.xpath(xpaths[brand]['subCat']).get(),
            False,
            gender,
            crawling=True)
        db.add(item)
        # next_url = urlsDb.nextUrl(response.url)
        # if next_url:
        #     print('NEXT:',next_url)
        #     yield response.follow(next_url, self.parse)
        # db.close()

def crawl():
    process = CrawlerProcess(
        settings={
            "USER_AGENT" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
        '''
            "BOT_NAME" : "molova_spider",
            "SPIDER_MODULES" : ["molova_spider.spiders"],
            "NEWSPIDER_MODULE" : "molova_spider.spiders",
            "ROBOTSTXT_OBEY" : "true",
            "DEFAULT_REQUEST_HEADERS" : {
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
                "Sec-Fetch-User": "?1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "navigate",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
            }
        '''
        }
    )
    process.crawl(ItemsSpider)
    process.start()

# Main code
scrap()
#crawl()

'''def strTo2DArray(string):
    vec = []
    for color in string.split("], ["):
        v = []
        print(len(vec))
        for image in color.split("', '"):
            image = image.replace('[[','').replace(']]','').replace("'",'')
            v.append(image)
        vec.append(v)
    return vec'''