import ast
import pytz
import requests
from time import sleep
from random import randint
from datetime import datetime

import pandas as pd

import Mango
import Stradivarius
import Zara
from Main import check_broken_links, post, sync

try:
    settings = ast.literal_eval(open('./Files/.settings','r').read())
except FileNotFoundError:
    settings = {'Mango': {'endpoints': [], 'endpoint': ''}, 'Stradivarius': {'endpoints': [], 'endpoint': ''}, 'Zara': {'endpoints': [], 'endpoint': ''}}
    with open('./Files/.settings','w') as s:
        s.write(str(settings))
try:
    old_urls = ast.literal_eval(open('./Files/.old_urls','r').read())
except (FileNotFoundError, SyntaxError):
    old_urls = []
    with open('./Files/.old_urls','w') as o:
        o.write('[]')
brands = [
    {'name': 'Mango', 'endpoint': settings['Mango']['endpoint'], 'endpoints': settings['Mango']['endpoints'], 'updates': True},
    {'name': 'Zara', 'endpoint': settings['Zara']['endpoint'], 'endpoints': settings['Zara']['endpoints'], 'updates': True},
    {'name': 'Stradivarius', 'endpoint': settings['Stradivarius']['endpoint'], 'endpoints': settings['Stradivarius']['endpoints'], 'updates': True}]

class Catcher:
    def __init__(self):
        self.tz = pytz.timezone('America/Bogota')
        self.today = f'{datetime.now(self.tz).day} - {datetime.now(self.tz).month}'
        self.columns = ['Hora', 'Cambió', 'Nuevos', 'Actualizados']
        self.filename = './Files/Catcher.xlsx'
        self.df = {}
        try:
            self.df = pd.read_excel(self.filename, sheet_name=None,engine='openpyxl')
        except FileNotFoundError:
            self.writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
            self.writer.save()
        loaded = False
        if f'{self.today} {brands[0]["name"]}' in self.df:
            loaded = True
        else:
            for brand in brands:
                self.df[f'{self.today} {brand["name"]}'] = pd.DataFrame(columns=self.columns)
        self.writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        if not loaded:
            for brand in brands:
                self.df[f'{self.today} {brand["name"]}'] = pd.DataFrame(columns=self.columns)
        for i,j in enumerate(self.df):
            self.df[j].to_excel(self.writer,j, index=False)
        self.writer.save()
        # self.check()

    def update_headers(self):
        self.session = requests.session()
        self.session.headers.update({
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'es-US,es;q=0.9',
            'content-type': 'application/json',
            'user-agent': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'][randint(0, 4)]})

    def write(self, data, brand):
        self.today = f'{datetime.now(self.tz).day} - {datetime.now(self.tz).month}'
        self.writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        try:
            self.df[f'{self.today} {brand}'].append(pd.Series(self.columns, index=self.columns), ignore_index=True)
        except:
            self.df[f'{self.today} {brand}'] = pd.DataFrame(columns=self.columns)
        self.df[f'{self.today} {brand}'] = self.df[f'{self.today} {brand}'].append(pd.Series(data, index=self.columns), ignore_index=True)
        for i, j in enumerate(self.df):
            self.df[j].to_excel(self.writer, j, index=False)
        self.writer.save()

    def check(self):
        count = 5
        for brand in brands:
            open(f'./Files/.changes_{brand["name"]}','w').close()
        while True:
            self.update_headers()
            for brand in brands:
                res = self.session.get(brand['endpoint']).json()
                new_data = res['products'] if brand['name'] == 'Stradivarius' else res['groups'][0]['garments'] if brand['name'] == 'Mango' else res['productGroups'][0]['elements']
                if type(new_data) is dict:
                    new_list = []
                    for _,key in enumerate(new_data):
                        new_list.append(new_data[key])
                    new_data = new_list
                if len(new_data) > 100:
                    new_data = new_data[:100]
                try:
                    data = ast.literal_eval(open(f'./Files/.changes_{brand["name"]}','r').read())
                except SyntaxError:
                    data = new_data
                new, updated = 0, 0
                for product in new_data:
                    product_exist, product_updated = False, False
                    if product in data:
                        product_exist = True
                    else:
                        for p in data:
                            try:
                                key = 'id' if brand['name'] == 'Zara' else 'name'
                                if product[key] == p[key]:
                                    product_exist, product_updated = True, True
                                    break
                            except:
                                print('ERROR')
                                with open(f'./Files/.changes_{brand["name"]}', 'w') as f:
                                    f.write(str(product))
                                break
                    if not product_exist:
                        new += 1
                    if product_updated:
                        updated += 1
                self.write([f'{datetime.now(self.tz).hour}:{datetime.now(self.tz).minute}', data != new_data, new, updated],brand['name'])
                brand['updates'] = brand['updates'] or data != new_data
                with open(f'./Files/.changes_{brand["name"]}', 'w') as f:
                    f.write(str(new_data))
            count += 1
            if count == 6:
                for brand in brands:
                    if brand['updates']:
                        print(f'Crawling {brand["name"]}')
                        exec(f'old_urls.extend({brand["name"]}.db.getAllUrls())')
                        with open('./Files/.old_urls', 'w') as o:
                            o.write(str(old_urls))
                        exec(f'{brand["name"]}.APICrawler(brand["endpoints"])')
                check_broken_links(crawling=True)
                post(crawling=True)
                count = 0
            sleep(randint(3000, 4000))


def scrap_links():
    for brand in brands:
        exec(f'{brand["name"]}.scrap_for_links()')

self = Catcher()
