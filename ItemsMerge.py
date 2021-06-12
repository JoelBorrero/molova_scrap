import Item, os, json

error = 0
totalItems = 0
percentage = 0
index = 0
bar = ""
path = "C:/Users/JoelBook/Documents/Molova/Database"
for file in os.listdir(path):
    if ".json" in file and not file == "Urls.json":
        with open(f"{path}/{file}", "r", encoding="utf8") as f:
            try:
                j = json.loads(f.read())
                totalItems+= len(j["Items"])
            except:
                pass
for file in os.listdir(path):
    if ".json" in file and not file == "Urls.json":
        with open(f"{path}/{file}", "r", encoding="utf8") as f:
            try:
                j = json.loads(f.read())
                for k in j["Items"]:
                    print(k)
                    for i in range(0):
                    # Item.Item(i['brand'],i['name'],i['description'],i['priceBefore'],i['allPricesNow'],i['discount'],i['allImages'],i['url'],i['allSizes'],i['colors'],i['category'],i['originalCategory'],i['subcategory'],i['originalSubcategory'],i['sale'],i['gender'])
                        print(i["brand"],i["name"])
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
                pass
input("\nPresione enter para salir\n")
