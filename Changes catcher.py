import ast
import pytz
import requests
from time import sleep
from random import uniform
from datetime import datetime

import pandas as pd


class Catcher:
    def __init__(self):
        self.tz = pytz.timezone('America/Bogota')
        self.today = f'{datetime.now(self.tz).day} - {datetime.now(self.tz).month}'
        self.columns = ['Hora','Cambió','Nuevos', 'Actualizados']
        self.filename = './Catcher.xlsx'
        self.df = {}
        try:
            self.df = pd.read_excel(self.filename, sheet_name=None,engine='openpyxl')
        except FileNotFoundError:
            self.writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
            self.writer.save()
        loaded = False
        if self.today in self.df:
            # self.df[self.today] = pd.Series(self.df[self.today], index=self.columns)
            # self.df[self.today].append(pd.Series(self.columns, index=self.columns), ignore_index=True)
            loaded = True
        else:
            self.df[self.today] = pd.DataFrame(columns=self.columns)
        self.writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        if not loaded:
            self.df[self.today] = pd.DataFrame(columns=self.columns)
        for i,j in enumerate(self.df):
            self.df[j].to_excel(self.writer,j, index=False)
        self.writer.save()
        open('./Changes data.txt','w').close()
        self.check()
    
    def update_headers(self):
        self.session = requests.session()
        self.session.headers.update({
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'es-US,es;q=0.9',
            'content-type': 'application/json',
            'cookie': 'ITXSESSIONID=182592649f55aa1d98689723945fba3c; _abck=98D0A42A991781EA9192E81AB1B3DA3F~-1~YAAQT/1Vvs+4hLh6AQAAeqNzSgaJEW8ixKACFBQiOORFishd5S4Qz7WkGyAvA0LNo/wTMQ4S6a5NkeaLagHp/t9Zbk9B6ga2UTgMBMhrC0rtyMirxcWjDCX8+hXQRF5Eex8lXYCu4V7H7HyTvSBPuK29LvIW3aFHvmqxw17hbJBndu67nAhdmxNNZ7r7wuqF861oo9dVhzLHYbhiBjPUmuOr5x22PV8HNtU3a15bH/pTOp/86mPMTWdWmmsO40hy/cFHprjRPILbrZqtt5zsZ46U6d+ODU2pGvwyvOXyIwQ4rSrPcBKcgmUw6Dtq/GBqlVzS9wfKc5RsbjAvn2anQyRSLhdS2ClIRGBc7knewLNuoBXxNrPFq3lPzdt5uXs=~-1~-1~-1; ak_bmsc=DD61DFF3B5C9D1B3E4463FEA8F6BDEC3~000000000000000000000000000000~YAAQT/1VvtC4hLh6AQAAeqNzSgzQJDKMApzD4ibQ2yO5D+QCMRHgTZRmSgabRaqtAeQTyqfPc0D1k3m0S66Jr5kvkwDl1rr1NNCyBLA+jZ83hwbE3Oq2KmOponQVKwsCHqbtQVS7W9Ne7/8kmLznO6z2fbKXtMG8Zntc+aeqY4eJ46PIzSdQPjrIoFu5zqPAOEbnSa99LDEcuJpIErezw5E+EDrbrh8n0OnL5xHzyiyTMYrq9uPKMfzzpM4NDUovIBvvN0TwGcDU0b6Ju+UlF9cqiMUhMaoLZCXw+RcFF/4aAhpstC8h5gJa4BCk/P7EIeBpOFJg9nKgWeqiP6Hkhh46mn3XN67SPHCt4/3iyVYumSCtiKryOQktUcVzkEO9V30=; bm_sz=972FA142E752B8D15050CD920326B68B~YAAQT/1VvtG4hLh6AQAAeqNzSgzXXX/95f+VvKgIwgtfU2OQW+ZMBBTicVhdB7msgrQ1jZ+P5pI1kwmpg3hmAD/29FxFdJTtw6yQTmmoLL8J2d2ZJj6JryxZIjM1uqDkZ7gy1mIP8kKwn61leSzqsZvRD+Zc5wYav5rroxMeNcFT0InjGA+juZx8ZtWfZ1PI5fD2iK1fDhUoZxcLAHJc5ALWycjN/fqV8WpnA+YJKNJVr7ePQncd0aNN3tLJGptKK49ts8dEtjYh2GbwUhuRRO5NQJCGvdpcpdjhTtruOEjQgrgevMA7naI=~3491394~3425845',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'referer': 'https://www.stradivarius.com/'})
    
    def write(self, data):
        self.today = f'{datetime.now(self.tz).day} - {datetime.now(self.tz).month}'
        self.writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        try:
            self.df[self.today].append(pd.Series(self.columns, index=self.columns), ignore_index=True)
        except:
            self.df[self.today] = pd.DataFrame(columns=self.columns)
        self.df[self.today] = self.df[self.today].append(pd.Series(data, index=self.columns), ignore_index=True)
        for i,j in enumerate(self.df):
            self.df[j].to_excel(self.writer,j, index=False)
        self.writer.save()

    def check(self):
        while True:
            self.update_headers()
            new_data = self.session.get('https://www.stradivarius.com/itxrest/2/catalog/store/55009615/50331099/category/1020093507/product?languageId=-48&appId=1').json()['products'][:20]
            try:
                data = ast.literal_eval(open('./Changes data.txt','r').read())
                new, updated = 0, 0
                for product in new_data:
                    product_exist, product_updated = False, False
                    if product in data:
                        product_exist = True
                    else:
                        for p in data:
                            if product['name'] == p['name']:
                                product_exist = True
                                product_updated = True
                                break
                    if not product_exist:
                        new += 1
                    if product_updated:
                        updated += 1
                self.write([f'{datetime.now(self.tz).hour}:{datetime.now(self.tz).minute}', data!=new_data, new, updated])
            except SyntaxError:
                print('Err')
                pass
            with open('./Changes data.txt','w') as f:
                f.write(str(new_data))
            sleep(uniform(1700, 2700))

self = Catcher()