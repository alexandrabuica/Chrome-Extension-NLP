import scrapy
from WebCrawler.items import NewspapercrawlerItem
from scrapy.selector import Selector 
from Extensie.summarizer import generate_summary 

class ScrapeRomaniaLibera(scrapy.Spider):
    name = "romanialibera"
    base_url = "https://romanialibera.ro/ultima-ora"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    def start_requests(self):
        yield scrapy.Request(url = self.base_url, headers = self.headers, callback = self.parse)


    def parse(self, response):
        sel = Selector(response) 
        article_headers = response.css('a[class="block"]::attr(href)').getall()
        for header in article_headers:
            source = 'https://romanialibera.ro/' + header
            yield scrapy.Request(source, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)
        item = NewspapercrawlerItem()
        source = response.url
        title = sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "font-bold", " " )) and contains(concat( " ", @class, " " ), concat( " ", "my-20px", " " ))]/text()').get().strip()
        header = sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "text-xl", " " ))]/text()').get().strip()
        image = response.css('div.relative img::attr(src)').get()
        article_body = sel.xpath('//*[(@id = "rl-article-content")]')
        sentences = []

        for p in article_body.xpath('.//p/text()'):
            sentences.append(p.get())

        content = header + " ".join(str(s) for s in sentences) 
        item['sursa'] = source
        item['titlu'] = title
        item['imagine'] = image
        item['corp'] = content
        item['rezumat'] = generate_summary(content, 2) 
        yield item

