from tinydb import TinyDB, Query, where
from Item import toInt

class Database:
    '''Creates a TinyDB database'''
    def __init__(self, name):
        TinyDB.default_table_name = "Items"
        self.db = TinyDB(f"./Database/{name}.json")
        self.urls_db = TinyDB("./Database/Urls.json")
        self.latest = TinyDB("./Database/Latest.json")
        self.q = Query()

    def add(self, item, debug=False):
        if not type(item) is dict:
            item = item.__dict__
        def update():
            categories = [
                "Camisas y Camisetas",
                "Pantalones y Jeans",
                "Vestidos y Enterizos",
                "Faldas y Shorts",
                "Abrigos y Blazers",
                "Ropa deportiva",
                "Zapatos",
                "Bolsos",
                "Accesorios",
            ]
            def transform(doc):
                for field in ["name","description","priceBefore","allPricesNow","discount","allSizes","sale", "colors", "url","allImages","category","subcategory", "allSizes"]:
                    if not doc[field] == item[field]:
                        doc[field] = item[field]
                for field in ["category", "originalCategory"]:
                    if not doc[field] in categories and item[field] in categories:
                        doc[field] = item[field]
            return transform
        it = self.contains(item["url"], str(item["allImages"]))
        if it:  # Update it
            self.db.update(update(), doc_ids=[it.doc_id])
            if debug:
                print('DB:Updating', it.doc_id)
            return int(it.doc_id)
        else:  # Create it
            if debug:
                print('DB:Adding',item["url"])
            item['url'] = normalyze_url(item['url'])
            self.addUrl(item['url'])
            return int(self.db.insert(item))

    def update_product(self, url, priceBfr, priceNow, discount):
        url = normalyze_url(url)
        print('updating',url)
        priceBfr = toInt(priceBfr)
        priceNow = toInt(priceNow)
        discount = toInt(discount)
        sale = priceNow < priceBfr
        if discount < 1 or discount >= 60:
            discount = (1-priceNow/priceBfr)*100
        if priceBfr > 0 and priceNow > 0:
            self.db.update({"priceBefore":priceBfr, "allPricesNow":[priceNow], 'discount':discount, 'sale':sale}, self.q.url == url)

    def addUrl(self, url):
        url = normalyze_url(url)
        if not self.urls_db.get(self.q.url == url):
            self.urls_db.insert({"url": url})
    def contains_url(self, url):
        return True if self.db.get(self.q.url == url) else False
    def contains(self, url, allImages=''):
        def matches(val, images):
            p = 0
            t = 0
            if val:
                if not type(val[0]) == list:
                    val=[val]
                for color in val:
                    for img in color:
                        try:
                            if img[:img.index('.jpg')+4] in images:
                                p += 1
                        except:
                            if img in images:
                                p += 1
                        t += 1
            return 0 if t==0 else p / t > 0.3
        def has_image(val, image):
            if 'pullandbear' in image:
                image = image[:image.index('_')]
            elif 'zara' in image:
                image = image[:image.index('/w/')]
            return image in str(val)
        url = normalyze_url(url)
        it = self.db.get(self.q.url == url)
        if not it:  # Search by imgs
            it = self.db.get(self.q.allImages.test(matches, allImages))
        if not it and allImages:
            it = self.db.get(self.q.allImages.test(has_image,allImages))
        if it:
            if not self.latest.get(self.q.url == it['url']):
                self.latest.insert({'url':it['url']})
        else:
            self.latest.insert({'url':url})
        return it

    def delete(self, url):
        self.db.remove(where('url') == url)

    def firstUrl(self):
        return self.urls_db.get(doc_id=1)["url"]

    def nextUrl(self, url):
        n = self.urls_db.get(self.q.url == url)
        try:
            n = self.urls_db.get(doc_id=n.doc_id + 1)["url"]
        except:
            return False
        return n

    def getAllUrls(self):
        '''Return a list with all urls in the Urls database'''
        res = []
        for url in self.db.all():
            res.append(url['url'])
        return res

    def get_crawl_urls(self, brands):
        mDb = Database("Mercedes Campuzano")
        zDb = Database("Zara")
        v=[]
        for o in self.urls_db.all():
            if any(b in o['url'] for b in brands):
                v.append(o["url"])
        return v
    
    def getAllItems(self):
        '''Return a list with all the items in the database'''
        return self.db.all()

    def getIdByUrl(self, url):
        '''Returns the `doc_id` of the given URL'''
        return int(self.db.get(self.q.url==url).doc_id)

    def close(self):
        self.db.close()
        self.urls_db.close()
    
def normalyze_url(url):
    try:
        return url[:url.index(".html")+5]
    except:
        return url