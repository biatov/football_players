from time import sleep
from scrapy import Selector
from ..items import PlaysItem
from scrapy.spiders import CrawlSpider
from selenium import webdriver
from pyvirtualdisplay import Display


class PlayersSpider(CrawlSpider):
    name = 'players'

    allowed_domains = ["footballindex.co.uk"]

    start_urls = ['https://www.footballindex.co.uk/stockmarket/home']

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1.5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

        selenium_response_text = self.driver.page_source
        new_selector = Selector(text=selenium_response_text)
        for each in new_selector.xpath('.//ng-include[@class="ng-scope"]').xpath('.//a[@ng-bind="player.name"]'):
            item = PlaysItem()
            item['player_name'] = each.xpath('text()').extract()
            yield item

        self.driver.close()
        self.display.stop()
