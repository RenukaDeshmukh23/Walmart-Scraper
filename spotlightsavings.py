# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.http import Request
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException

class SpotlightsavingsSpider(scrapy.Spider):
    name = 'spotlightsavings'
    allowed_domains = ['walmart.com']
    #start_urls = ['https://www.walmart.com/m/savings-spotlight']

    def start_requests(self):
        self.driver = webdriver.Chrome('F:/chromedriver')
        self.driver.get('https://www.walmart.com/m/savings-spotlight')
        self.driver.maximize_window()
        response = Selector(text=self.driver.page_source)

    #def parse(self, response):
        URLs = response.xpath("//*[@class='product-title-link line-clamp line-clamp-3']//@href").extract()
        for Url in URLs:
            #absolute_URL = response.urljoin(Url)
            absolute_URL="https://www.walmart.com"+Url
            #self.driver.get(absolute_URL)
            #yield{'url':absolute_URL}
            yield Request(absolute_URL, callback=self.parse_products)

        while True:
            try:
                next = self.driver.find_element_by_xpath('//*[@class="paginator-btn paginator-btn-next"]')
                sleep(5)
                next.click()
                sleep(5)
                response = Selector(text=self.driver.page_source)
                URLs = response.xpath("//*[@class='product-title-link line-clamp line-clamp-3']//@href").extract()
                for Url in URLs:
                    #absolute_URL = response.urljoin(Url)
                    absolute_URL="https://www.walmart.com"+Url
                    #self.driver.get(absolute_URL)
                    #yield{'url':absolute_URL}
                    yield Request(absolute_URL, callback=self.parse_products)

            except NoSuchElementException:
                print('No more pages to load.')
                self.driver.quit()

    def parse_products(self,response):
        Name = response.xpath('//*[@class="prod-ProductTitle prod-productTitle-buyBox font-bold"]//text()').extract()
        Price = response.xpath('//*[@itemprop="price"]//text()').extract_first()
        Ratings = response.xpath('//*[@itemprop="ratingValue"]//text()').extract_first()

        yield{'Name':Name,
        'Price':Price,
        'Ratings':Ratings}
