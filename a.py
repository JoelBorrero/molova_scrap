from Database import Database

db = Database("Gef")
print(db.getAllUrls())


'''
Deprecated functions
def upload(lastLoad, uploadAll=False):
    import boto3
    from Private import private
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
'''