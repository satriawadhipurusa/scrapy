import scrapy

class TagsSpider(scrapy.Spider):
	name = "tags"

	def start_requests(self):
		url = 'http://quotes.toscrape.com/'
		tag = getattr(self, 'tag', None)
		if tag is not None:
			url = url + 'tag/' + tag
		yield scrapy.Request(url, self.parse)

	def parse(self, response):
		for quote in response.css('div.quote'):
			yield{
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first()
			}

		for a in response.css('li.next a'):
			yield response.follow(a, callback=self.parse)