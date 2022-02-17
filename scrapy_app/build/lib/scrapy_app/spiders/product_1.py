import os
import csv
import glob
import pymysql
import scrapy
import logging
import datetime
from .readdata import dataReader
import shutil


class Product1Spider(scrapy.Spider):
    name = 'product_1'
    allowed_domains = ['www.skroutz.gr']
    # start_urls = ['https://www.skroutz.gr/s/13878315/Vogue-VO-5212S-W44-87.html',
    #                  'https://www.skroutz.gr/s/20314550/Arnette-El-Carmen-AN4263-265887-Matte-Black.html',
    #                  'https://www.skroutz.gr/s/6585825/Arnette-AN4007-01.html?from=catspan',
    #                  'https://www.skroutz.gr/s/16035327/Bausch-Lomb-EasySept-360ml-120ml.html',
    #                  'https://www.skroutz.gr/s/24403771/Ralph-Lauren-PH2224-5017.html',
    #                  'https://www.skroutz.gr/s/8414500/Alcon-Opti-Free-PureMoist-300ml-60ml.html',
    #                  'https://www.skroutz.gr/s/12109270/Bausch-Lomb-ReNu-Multiplus-360ml-60ml.html',
    #                  'https://www.skroutz.gr/s/16035327/Bausch-Lomb-EasySept-360ml-120ml.html',
    #                  'https://www.skroutz.gr/s/6869602/Alcon-Opti-Free-Express-355ml.html',
    #                  'https://www.skroutz.gr/s/6935506/Avizor-Ever-Clean-Pure-225ml.html',
    #                  'https://www.skroutz.gr/s/11878545/Bausch-Lomb-Biotrue-360ml-extra-Bottle-60ml.html',
    #                  'https://www.skroutz.gr/s/26087654/Soleko-Biosee-Clear-All-In-One-Solution-380ml.html',
    #                  'https://www.skroutz.gr/s/15079953/Amvis-AquaSoft-380ml-Extra-Bottle-60ml.html']

    start_urls = dataReader()
    def parse(self, response):

        urls = [1]
        for url in urls:
            product = response.xpath("//*[@id=\"sku-details\"]/div[2]/div[2]/div[1]/h1/text()").get()
            my_price = response.xpath("//*[@id=\"shop-6264\"]/div[2]/div/strong/text()").get()
            my_productName = response.xpath("//*[@id=\"shop-6264\"]/div[1]/div[3]/div/h3/a/text()").get()
            myAvailability = response.xpath("//*[@id=\"shop-6264\"]/div[1]/div[2]/div/p/span").get()
            companyName = response.xpath("//*[@id=\"prices\"]/li[1]").get()
            price = response.xpath("//*[@id=\"prices\"]/li[1]/div[2]/div[1]/strong/text()").get()
            bestPriceAvailability = response.xpath("//*[@id=\"prices\"]/li[1]/div[1]/div[2]/div[1]/p/span/text()").get()
            date = datetime.datetime.now()
            is_non_empty = bool(my_price)
            if  is_non_empty:
                print("it's ok")
            else:
                my_price = 'Not_Available'
                my_productName = 'Not_Available'
            print(product)
            print(my_price)
            print(my_productName)
            print(companyName)
            print(price)
            yield {
                'product': product,
                'my_price': my_price.replace(" €", "").replace(",", ".").replace("Not_Available", ""),
                'my_productName': my_productName,
                'my_availability': myAvailability,
                'company': companyName[:18].replace("\"", "").replace("<li id=shop-", "").replace(" ", ""),
                'price' : price.replace(" €", "").replace(",", "."),
                'bestPriceAvailability' : bestPriceAvailability,
                'date': date
            }

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        mydb = pymysql.connect(host = 'localhost',
                               user = 'root',
                               passwd = '',
                               db = 'skroutz_4')
        cursor = mydb.cursor()

        csv_data = csv.reader(open(csv_file, encoding="utf8"))
        cursor.execute('TRUNCATE TABLE api_datamaintable')




        row_count = 0
        for row in csv_data:
            if row_count != 0:
                cursor.execute('INSERT IGNORE INTO api_datamaintable (product, my_price, my_productName, my_availability, company, price, bestPriceAvailability, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', row)
                cursor.execute('INSERT IGNORE INTO api_datamaintable_alldata (product, my_price, my_productName, my_availability, company, price, bestPriceAvailability, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', row)
            row_count += 1

        mydb.commit()
        cursor.close()
        file = csv_file
        f = open(file, "w+")
        f.close()