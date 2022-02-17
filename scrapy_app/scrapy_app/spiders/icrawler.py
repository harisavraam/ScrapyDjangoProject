# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import os
import csv
import glob
import pymysql
import scrapy
import logging
import datetime
from .readdata import dataReader
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import shutil
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

class IcrawlerSpider(scrapy.Spider):


    name = 'icrawler'
    allowed_domains = ['www.skroutz.gr']
    start_urls = dataReader()
    # start_urls = ['https://www.skroutz.gr/s/13878315/Vogue-VO-5212S-W44-87.html']


    # rule = (
    #     Rule(LinkExtractor(allow=r'Items/', callback='parse_item', follow=True))
    # )
    # def __init__(self, *args, **kwargs):
    #     IcrawlerSpider.rules = [
    #         Rule(LinkExtractor(unique=True), callback='parse'),
    #     ]
    #     super(IcrawlerSpider, self).__init__(*args, **kwargs)



    def parse(self, response):
            product = response.xpath("//*[@id=\"sku-details\"]/div[2]/div[2]/div[1]/h1/text()").get()
            my_price = response.xpath("//*[@id=\"shop-6264\"]/div[2]/div/strong/text()").get()
            my_productName = response.xpath("//*[@id=\"shop-6264\"]/div[1]/div[3]/div/h3/a/text()").get()
            myAvailability = response.xpath("//*[@id=\"shop-6264\"]/div[1]/div[2]/div/p/span").get()
            companyName = response.xpath("//*[@id=\"prices\"]/li[1]").get()
            price = response.xpath("//*[@id=\"prices\"]/li[1]/div[2]/div[1]/strong/text()").get()
            bestPriceAvailability = response.xpath("//*[@id=\"prices\"]/li[1]/div[1]/div[2]/div[1]/p/span/text()").get()
            date = datetime.datetime.now()
            print("product: ", product, ",my_price: ",my_price, ",my_productName :"
                  ,my_productName, ",myAvailability :", myAvailability, ",companyName :", companyName
                  , ",price :", price, ",date :", date, "End")


            # product = str(product).encode('utf-8')
            # my_price = str(my_price).encode('utf-8')
            # my_productName = str(my_productName).encode('utf-8')
            # myAvailability = str(myAvailability).encode('utf-8')
            # companyName = str(companyName).encode('utf-8')
            # price = str(price).encode('utf-8')
            # bestPriceAvailability = str(bestPriceAvailability).encode('utf-8')



            is_non_empty = bool(my_price)
            if  is_non_empty:
                print("it's ok")
            else:
                my_price = 'Not_Available'
                my_productName = 'Not_Available'
            is_non_empty_2 = bool(myAvailability)
            if is_non_empty_2:
                print("Availabilities are fixed")
            else:
                myAvailability = 'N/A'
                bestPriceAvailability = 'N/A'
            print(product)

            is_non_empty_3 = bool(companyName)
            if is_non_empty_3:
                print("Product is available")
            else:
                companyName = 'N/A'
                price = 'N/A'
            # print(my_price)
            # print(my_productName)
            # print(companyName)
            # print(price)
            yield {
                'product': str(product),
                'my_price': str(my_price).replace(" €", "").replace(",", ".").replace("Not_Available", ""),
                'my_productName': str(my_productName),
                'my_availability': str(myAvailability),
                'company': str(companyName)[:18].replace("\"", "").replace("<li id=shop-", "").replace(" ", ""),
                'price' : str(price).replace(" €", "").replace(",", "."),
                'bestPriceAvailability' : str(bestPriceAvailability),
                'date': date
            }
            print(" product is :", product, "my_price is : ", my_price )



    # def close(self, reason):
    #     csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
    #     mydb = pymysql.connect(host = 'localhost',
    #                            user = 'root',
    #                            passwd = '',
    #                            db = 'skroutz_4')
    #     cursor = mydb.cursor()
    # #
    #     csv_data = csv.reader(open(csv_file, encoding="utf8"))
    #     cursor.execute('TRUNCATE TABLE api_datamaintable')
    # #
    # #
    # #
    # #
    #     row_count = 0
    #     for row in csv_data:
    #         if row_count != 0:
    #             cursor.execute('INSERT IGNORE INTO api_datamaintable (product, my_price, my_productName, my_availability, company, price, bestPriceAvailability, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', row)
    #             cursor.execute('INSERT IGNORE INTO api_datamaintable_alldata (product, my_price, my_productName, my_availability, company, price, bestPriceAvailability, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', row)
    #         row_count += 1
    # #
    #     mydb.commit()
    #     cursor.close()
    #     file = csv_file
    #     f = open(file, "w+")
    #     f.close()

#
# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# runner = CrawlerRunner()
# d = runner.crawl(IcrawlerSpider)
# d.addBoth(lambda _: reactor.stop())
# reactor.run() # the script will block here until the crawling is finished









