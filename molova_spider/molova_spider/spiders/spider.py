import scrapy, sys  
sys.path.append("C:/Users/JoelBook/Documents/Molova")
from Item import Item, toInt

file = 'C:/Users/JoelBook/Documents/Molova/Items/Crawled.txt'
xpaths={
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
        'hasStock'      : '',
        },
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
        'hasStock'      : '',
        },
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
        'name'          : './/h1[@class="product-detail-info__name"]/text()',
        'priceBefore'   : './/div[@class="product-detail-info__price-amount price"]/span[@class="price__amount price__amount--old"]/text()',
        'priceBefore2'  : './/span[@class="price__amount"]/text()',
        'priceNow'      : './/div[@class="product-detail-info__price-amount price"]/span[@class="price__amount price__amount--on-sale"]/text()',
        'sizes'         : './/ul[contains(@id,"product-size-selector-product-detail-info-")]/li/div/div/span/text()',
        'stock'         : './/ul[contains(@id,"product-size-selector-product-detail-info-")]/li/@class',
        'subCat'        : './/div[@class="expandable-text__inner-content"]/p/text()',
        'hasStock'      : 'item--is-disabled',
        }
}
class ItemsSpider(scrapy.Spider):
    name = "Items"
    #user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
    start_urls = [
        #"https://www.zara.com/co/es/vestido-camisero-rayas-p02462253.html",
        #"https://www.stradivarius.com/co/new-collection/ropa/compra-por-producto/camisetas/ver-todo/basic-cropped-polo-shirt-c1020047036p302168037.html?colorId=045",
        "https://www.bershka.com/co/mujer/ropa/pantalones/pantal%C3%B3n-sarga-straight-rotos-c1010193216p102707131.html",
        #"https://www.mercedescampuzano.com/bota-maximus-beige/p",
        # "https://www.mercedescampuzano.com/tenis-goose-negro/p",
        # "https://www.mercedescampuzano.com/baleta-tacon-ina-beige/p",#SALE
    ]

    def parse(self, response):
        headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}
        if 'bershka' in response.url:
            brand = 'Bershka'
        elif 'gef' in response.url:
            brand = 'Gef'
        elif 'mercedes' in response.url:
            brand = 'Mercedes Campuzano'
        elif 'Zara' in response.url:
            brand = 'Zara'
        else:
            brand = 'Brand'
        gender = 'Hombre' if 'hombre' in response.url else 'Mujer'
        scrapy.http.Request("https://www.bershka.com/co/mujer/ropa/pantalones/pantal%C3%B3n-sarga-straight-rotos-c1010193216p102707131.html", method='GET' , headers = headers,  dont_filter=False)
        try:
            with open("C:/Users/JoelBook/Documents/Molova/Items/Crawled.txt","a",encoding="utf8") as f:
                f.write(str(response.body))
        except Exception as e:
            print('ERROR                    NEVER PRINTS BODY>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',e)

        '''
        temp = [response.xpath(xpaths[brand]['sizes']).getall(),response.xpath(xpaths[brand]['stock']).getall()]
        sizes = []
        for i in range(len(temp[0])):
            if xpaths[brand]['hasStock'] in temp[1][i]:
                sizes.append('{}(Agotado)'.format(temp[0][i]))
            else:
                sizes.append(temp[0][i])
        temp.clear()
        priceNow = toInt(response.xpath(xpaths[brand]['priceNow']).getall())
        priceBefore = toInt(response.xpath(xpaths[brand]['priceBefore']).getall())
        if priceBefore == '$ 0':
            priceBefore = toInt(response.xpath(xpaths[brand]['priceBefore2']).getall())
            if priceBefore == '$ 0':
                priceBefore = priceNow
        Item(brand,response.xpath(xpaths[brand]['name']).get(),
            response.xpath(xpaths[brand]['description']).get(),
            priceBefore,
            priceNow,
            ''.join(response.xpath(xpaths[brand]['discount']).getall()).replace('\xa0',''),
            response.xpath(xpaths[brand]['imgs']).getall(),
            response.url,
            sizes,
            response.xpath(xpaths[brand]['color']).get(),
            response.xpath(xpaths[brand]['category']).get(),
            response.xpath(xpaths[brand]['category']).get(),
            response.xpath(xpaths[brand]['subCat']).get(),
            response.xpath(xpaths[brand]['subCat']).get(),
            False,
            gender,
            crawling=True)'''