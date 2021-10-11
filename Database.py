import ast
from tinydb import TinyDB, Query, where
from Item import toInt
from JoelDB import JoelDB

class Database:
    '''Creates a TinyDB database'''
    def __init__(self, name):
        TinyDB.default_table_name = 'Items'
        self.db = TinyDB(f'./Database/{name}.json')
        self.latest = TinyDB('./Database/Latest.json')
        self.broken = JoelDB('Broken')
        self.q = Query()

    def add(self, item, debug=False, sync=False):
        try:
            item['allImages']
        except:
            item = item.__dict__
        for key in ['allImages', 'allSizes', 'colors']:
            item[key] = ast.literal_eval(str(item[key]))
        if item['allImages'] and item['allImages'][0]:
            def update():
                categories = [
                    'Camisas y Camisetas',
                    'Pantalones y Jeans',
                    'Vestidos y Enterizos',
                    'Faldas y Shorts',
                    'Abrigos y Blazers',
                    'Ropa deportiva',
                    'Zapatos',
                    'Bolsos',
                    'Accesorios',]
                def transform(doc):
                    for field in ['name', 'description', 'priceBefore', 'allPricesNow', 'discount', 'allSizes', 'sale', 'colors', 'url', 'allImages', 'category', 'subcategory', 'allSizes']:
                        if not doc[field] == item[field]:
                            doc[field] = item[field]
                    for field in ['category', 'originalCategory']:
                        if not doc[field] in categories and item[field] in categories:
                            doc[field] = item[field]
                return transform
            it = self.contains(item['url'], str(item['allImages']), sync)
            if item['allSizes'] and all([all(['(AGOTADO)' in size for size in sizes]) for sizes in item['allSizes']]):
                self.delete(item['url'])
                self.broken.add(item['url'])
            if it:  # Update it
                if all([all(['(AGOTADO)' in size for size in sizes]) for sizes in it['allSizes']]):
                    self.delete(it['url'])
                    return self.broken.add(it['url'])
                if item['url'] != it['url']:
                    self.broken.add(it['url'])
                self.db.update(update(), doc_ids=[it.doc_id])
                return int(it.doc_id)
            else:  # Create it
                item['url'] = normalyze_url(item['url'])
                return int(self.db.insert(item))

    def update_product(self, elem, url, XPATHS={}):
        '''Update the item if its exists in database
            `elem`: Web element
            `url`: Url
            `XPATHS`: Dictionary with XPATHS locators'''
        url = normalyze_url(url)
        if elem.__class__ is list:
            discount, priceBfr, priceNow = elem
        else:
            priceNow = elem.find_element_by_xpath(XPATHS['fast_priceNow']).text
            try:
                priceBfr = elem.find_element_by_xpath(XPATHS['fast_priceBfr']).text
                discount = elem.find_element_by_xpath(XPATHS['fast_discount']).text
            except:
                priceBfr = priceNow
                discount = 0
        priceBfr = toInt(priceBfr)
        priceNow = toInt(priceNow)
        discount = toInt(discount)
        # print(priceBfr, priceNow, discount, url)
        sale = priceNow < priceBfr
        if discount < 1 or discount >= 60:
            discount = (1 - priceNow / priceBfr) * 100 if priceBfr else 0
        if priceBfr > 0 and priceNow > 0:
            self.db.update({'priceBefore':priceBfr, 'allPricesNow':[priceNow], 'discount':discount, 'sale':sale}, self.q.url == url)

    def contains_url(self, url):
        return True if self.db.get(self.q.url == url) else False
        
    def contains(self, url, allImages='', sync=False):
        def has_image(val, image):
            if 'pullandbear' in image:
                image = image[:image.index('_')]
            elif 'zara' in image:
                image = image[:image.index('/w/')]
            elif 'stradivarius' in image:
                image = image[:image.rindex('_')]
            if '.jpg?t' in image:
                image = image[:image.index('.jpg?t') + 4]
            return image in str(val)
        print(url)
        url = normalyze_url(url)
        print(url)
        it = self.db.get(self.q.url == url)
        print(it)
        if not it and allImages: # Search by imgs
            print('allimgs')
            it = self.db.get(self.q.allImages.test(has_image,allImages))
        if not sync:
            if it:
                print('it')
                if not self.latest.get(self.q.url == it['url']):
                    self.latest.insert({'url':it['url']})
            else:
                print('else')
                self.latest.insert({'url':url})
        print(it)
        return it

    def delete(self, url):
        self.db.remove(where('url') == url)

    def clear(self):
        self.db.remove(self.q.url != '')

    def getAllUrls(self):
        '''Return a list with all urls in the Urls database'''
        res = []
        for url in self.db.all():
            res.append(url['url'])
        return res
    
    def getAllItems(self):
        '''Return a list with all the items in the database'''
        return self.db.all()

    def getIdByUrl(self, url):
        '''Returns the `doc_id` of the given URL'''
        return int(self.db.get(self.q.url==url).doc_id)

    def close(self):
        self.db.close()
    
def normalyze_url(url):
    try:
        if 'pullandbear' in url:
            return url[:url.index('?cS=')]
        return url[:url.index('.html')+5]
    except ValueError:
        return url