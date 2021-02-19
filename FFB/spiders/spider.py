import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from ..items import FfbItem

pattern = r'(\r)?(\n)?(\t)?(\xa0)?'


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    start_urls = ['https://www.ffb.at/public/presse.html']

    def parse(self, response):


        articles = response.xpath('//div[@class="presseBox"]')
        items = []
        for article in articles:
                item = ItemLoader(FfbItem())
                item.default_output_processor = TakeFirst()
                date = article.xpath('.//div[@class="date"]/text()').get()
                title = article.xpath('.//h3//text()').get()
                content = article.xpath('.//div[@class="presseText"]//text()').getall()
                content = [text.strip() for text in content]
                content = re.sub(pattern, "",' '.join(content))



                item.add_value('date', date)
                item.add_value('title', title)
                item.add_value('link', response.url)
                item.add_value('content', content)
                items.append(item.load_item())
        return items
