# -*- coding: utf-8 -*-
import scrapy
from ..items import RiyasewanaItem
from scrapy.http import Request
from datetime import datetime
import time


postedList= []
reading_max = None


class SpydiSpider(scrapy.Spider):
    name = 'spider1'
    page_number = 2
    start_urls = ['https://riyasewana.com/search']
    
    
    def parse(self, response):
        
        global reading_max
        if reading_max == None:
            reading_max =  fileRead()
            
        # identify the total number of web pages
        max_page_number = response.css(
            'br+ .pagination a:nth-child(21)::text').extract()
        res = str("".join(map(str, max_page_number)))
        temp_maxPage = res.replace('.', '')
        max_pages = int(temp_maxPage)

        # links of detail page of products
        product_detailed_link = response.css('.more a::attr(href)').extract()
      
        for item in product_detailed_link:

            yield scrapy.Request(
                response.urljoin(item),
                callback=self.parse_page2
            )
       
        next_page = 'https://riyasewana.com/search?page=' + \
            str(SpydiSpider.page_number)+''
        if SpydiSpider.page_number <= 10:  # add 'max_pages' when you need to scrape all the pages
            SpydiSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
        
    def parse_page2(self, response):
       
        product_contact_number = response.css(
            '.tfiv:nth-child(2) .moreph::text').extract()
        for item in product_contact_number:
            product_contact_number_list = item.strip('[')
        product_contact_name = response.css(
            '.tfiv~ .tfiv .moreph::text').extract()
        for item in product_contact_name:
            product_contact_name_list = item.strip('[')
        product_name = response.css('h1::text').extract()
        for item in product_contact_name:
            product_source = 'riyasewana.com'
        for item in product_name:
            product_name_list = item.strip('[')
        product_price = response.css(
            'tr:nth-child(5) .aleft:nth-child(2)::text').extract()
        for item in product_price:
            product_price_list = item.strip('[')
        product_area = response.css(
            'tr:nth-child(4) .aleft:nth-child(2)::text').extract()
        for item in product_area:
            product_area_list = item.strip('[')
      
        product_posted_time = response.css('time::text').extract()
        for item in product_posted_time: 
            # identifying the posted time
            product_posted_time_list = item.strip('[')
            post_time = datetime.strptime(item,'%Y %b %d %I:%M %p')
            
            # identifying the current time
            now = datetime.now()
            item_current_time = now.strftime('%H:%M')
            print('current time:',item_current_time)
            
            # formatting the posted time to a formal format
            for s in product_posted_time_list: 
                s = post_time
            string = item[12:]
            in_time = datetime.strptime(string, "%I:%M %p")
            post_time = datetime.strftime(in_time, "%H:%M")
            print('Posted time:',post_time)
            print('s:',s)
            print('reading_max:',reading_max)
            
        # deciding what is the max posted time    
        postedList.append(s) 
        max_posted = max(postedList)
        
        # comparing the previous max posted time with the current posted time    
        if s > reading_max:
            
            post_time = RiyasewanaItem()
           
            post_time['product_contact_name'] = product_contact_name_list
            post_time['product_contact_number'] = product_contact_number_list
            post_time['product_area'] = product_area_list
            post_time['product_name'] = product_name_list
            post_time['product_posted_time'] = s
            post_time['product_price'] = product_price_list
            post_time['product_source'] = product_source

            print('Max posted:',max_posted)  
            yield post_time

        else:
            print('Already stored')
        
        # calling the fileWriter method to write 
        fileWrite(max_posted)      
        
# writting the maximum posted time to a text file            
def fileWrite(max_pos):
    saveFile = open('max_posted.txt','w')
    sace = str(max_pos)
    saveFile.write(sace)
    saveFile.close()
 
# reading the maximum posted time from the text file                 
def fileRead():
    with open('max_posted.txt', 'r') as f:
        maxx = f.read()
        maxx_post = datetime.strptime(maxx,'%Y-%m-%d %H:%M:%S')
        print('maxx_post', maxx_post)
        return maxx_post
    print(f.closed)   
        