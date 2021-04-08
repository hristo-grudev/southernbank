import scrapy

from scrapy.loader import ItemLoader

from ..items import SouthernbankItem
from itemloaders.processors import TakeFirst


class SouthernbankSpider(scrapy.Spider):
	name = 'southernbank'
	start_urls = ['https://www.southernbank.com/blog']

	def parse(self, response):
		post_links = response.xpath('//a[@rel="bookmark"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="karma-pages"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="entry-title"]/text()').get()
		description = response.xpath('//div[@class="post_content"]/p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="post_date"]//text()[normalize-space()]').getall()
		date = [p.strip() for p in date if '{' not in p]
		date = ' '.join(date).strip()

		item = ItemLoader(item=SouthernbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
