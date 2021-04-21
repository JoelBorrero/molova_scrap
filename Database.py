from tinydb import TinyDB, Query

class Database:
    def __init__(self, name):
        TinyDB.default_table_name = "Items"
        self.db = TinyDB(f"./Database/{name}.json")
        self.urls_db = TinyDB("./Database/Urls.json")
        self.q = Query()

    def add(self, item):
        item = item.__dict__
        def matches(val, images):
            p = 0
            t = 0
            for color in val:
                for img in color:
                    if img in images:
                        p += 1
                    t += 1
            return p / t > 0.5
   
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
                for field in ["name","description","priceBefore","allPricesNow","discount","allSizes","sale"]:
                    if not doc[field] == item[field]:
                        doc[field] = item[field]
                for field in ["category", "originalCategory"]:
                    if not doc[field] in categories and item[field] in categories:
                        doc[field] = item[field]
            return transform
        # try:
        it = self.db.get(self.q.url == item["url"])
        if not it:  # Search by imgs
            it = self.db.get(self.q.allImages.test(matches, str(item["allImages"])))
        if it:  # Update it
            print('DB:Updating', it.doc_id)
            self.db.update(update(), doc_ids=[it.doc_id])
        else:  # Create it
            print('DB:Adding')
            self.db.insert(item)
    # except Exception as e:
        # print('ERROR>>>>>>>>>>>>>>>>>>>>>>>>>',item['name'],e)
        # self.urlError(item['url'])

    def addUrl(self, url):
        if not self.urls_db.get(self.q.url == url):
            self.urls_db.insert({"url": url, "errors": 0})

    def urlError(self, url):
        u = self.urls_db.get(self.q.url == url)
        self.urls_db.update({"errors": u["errors"] + 1}, doc_ids=[u.doc_id])

    def contains(self, url):
        return self.urls_db.contains(self.q.url == url)

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
        v=[]
        for o in self.urls_db.all():
            v.append(o["url"])
        return v
    
    def getAllItems(self):
        '''Return a list with all the items in the database'''
        return self.db.all()

        
    def close(self):
        self.db.close()
        self.urls_db.close()