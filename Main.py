from Private import private
import os, boto3, time
import Bershka, Gef, MercedesCampuzano, PullAndBear, Stradivarius, Zara
def upload(lastLoad):
    access_key = private['access_key']
    secret_access_key = private['secret_access_key']
    bucket = 'recursosmolova'
    client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)
    path = 'C://Users/JoelBook/Documents/Molova/Items'
    for file in os.listdir(path):
        if '.json' in file:
            name = 'Items/{}'.format(str(file))
            if os.path.getmtime('{}/{}'.format(path,file))>lastLoad:
                client.upload_file('{}/{}'.format(path,file), bucket, name)
                print('Uploading',file)
            else:
                pass
    return time.time()
lastLoad = time.time()
brands = [
    #'Bershka',
    'Stradivarius',#'MercedesCampuzano',
    'Gef','Zara','PullAndBear'
    ]
for brand in brands:
    try:
        exec('{}.Scrap{}()'.format(brand, brand))
    except:
        print('Error scrapping',brand)
    lastLoad = upload(lastLoad)