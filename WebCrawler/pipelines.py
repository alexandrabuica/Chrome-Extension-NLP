# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class NewspapercrawlerPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='1234',
            database='Extensie'
        )
        self.table_cursor = self.conn.cursor()

    def create_table(self):
        self.table_cursor.execute("""DROP TABLE IF EXISTS Articole""")
        self.table_cursor.execute("""CREATE TABLE Articole(
           id INT auto_increment primary key,
           titlu text,
           sursa text,
           corp text,
           rezumat text,
           imagine text
        )""")

    def store_db(self, item):
        self.table_cursor.execute("""INSERT INTO Articole (titlu, sursa, corp, rezumat, imagine) VALUES (%s, %s, %s, %s, %s)""", (
            item['titlu'],
            item['sursa'],
            item['corp'],
            item['rezumat'],
            item['imagine'] 
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item