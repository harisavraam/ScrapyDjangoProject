
import json
import mysql.connector
import pymysql
import mysql.connector

# class ScrapyAppPipeline(object):
#     def __init__(self, *args, **kwargs):
#         self.items = []
#
#
#     def close_spider(self, spider):
#             item = DataMainTable()
#             item.data = json.dumps(self.items)
#             item.save()
#
#     def process_item(self, item, spider):
#         return item


class ScrapyAppPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(
                host = 'localhost',
                user = 'root',
                passwd = '',
                db = 'skroutz_4'
            )
        self.curr = self.conn.cursor()


    # def create_table(self):
    #     self.curr.execute("""DROP TABLE IF EXISTS quotes_tb""")
    #     self.curr.execute("""create table quotes_tb(
    #                     title text,
    #                     author text,
    #                     tag text)""")

    def process_item(self, item, spider):
        self.curr.execute("""INSERT IGNORE INTO api_datamaintable (product, my_price, my_productName, my_availability, company, price, bestPriceAvailability, date) values (%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item.get('product'),
            item.get('my_price'),
            item.get('my_productName'),
            item.get('my_availability'),
            item.get('company'),
            item.get('price'),
            item.get('bestPriceAvailability'),
            item.get('date')
            ))
        self.curr.execute("""INSERT IGNORE api_datamaintable_alldata (product, my_price, my_productName, my_availability, company, price, bestPriceAvailability, date) values (%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item.get('product'),
            item.get('my_price'),
            item.get('my_productName'),
            item.get('my_availability'),
            item.get('company'),
            item.get('price'),
            item.get('bestPriceAvailability'),
            item.get('date')
            ))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.curr.close()
        self.conn.close()