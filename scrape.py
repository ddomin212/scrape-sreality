import scrapy
import json
import psycopg2


class MySpider(scrapy.Spider):
    name = 'Real estate data of srealty.cz'
    conn = psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password="secret",
        port=5432
    )
    cur = conn.cursor()
    max_pages = 1
    base_api_url = 'https://www.sreality.cz/api'

    start_urls = ['https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=' + str(50) + '&page='+str(x)+''for x in range(1, 11)]
  
    def parse(self, response):
         jsonresponse = response.json() 

         for item in jsonresponse["_embedded"]['estates']:
             yield scrapy.Request( self.base_api_url + item['_links']['self']['href'] ,
                          callback=self.parse_detail_page)
         
             
    def add_postgres(self, title, img1, img2, img3):
        print('Adding to postgres: ', title, img1, img2, img3)
        try:
            insert_command = "INSERT INTO sreality_table (name, img1, img2, img3) VALUES (%s, %s, %s, %s)"
            self.cur.execute(insert_command, (title, img1, img2, img3))
            self.conn.commit()
            
        except Exception as e:
            print('Error: ', e)

    def handle_results(self, item):
        print(item)
        self.add_postgres(item['TITLE'], item['IMAGES'][0], item['IMAGES'][1], item['IMAGES'][2])

    def spider_closed(self, spider):
        # Whatever is here will run when the spider is done.
        self.cur.close()
        self.conn.close()

    def parse_detail_page(self, response):  
        jsonresponse = response.json()        
        item = {} # empty item as distionary
        try:             

            item['TITLE'] = jsonresponse['name']['value']

            # gather images
            item['IMAGES'] = []
            for images in jsonresponse['_embedded']['images'][:3]:                 
                if images['_links']['self']:
                    item['IMAGES'].append(images['_links']['self']['href'])
        except Exception as e:
            print ('Error: ' , e, '. for url: ',   response.url  )
        self.handle_results(item)
        yield item  

def start_crawler():
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess()
    results = process.crawl(MySpider)
    process.start()