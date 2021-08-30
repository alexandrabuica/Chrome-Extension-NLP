import scrapy
from WebCrawler.items import NewspapercrawlerItem
from scrapy.selector import Selector 
from Extensie.summarizer import generate_summary 

class ScrapeJurnalulNational(scrapy.Spider):
    name = "jurnalul"
    base_url = "https://jurnalul.ro/stiri/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    def start_requests(self):
        yield scrapy.Request(url = self.base_url, headers = self.headers, callback = self.parse)

    def parse(self, response):
        sel = Selector(response)
        article_headers = sel.xpath('//h2//a')
        for header in article_headers:
            source = "https://jurnalul.ro/" + header.xpath('@href').extract()[0]
            yield scrapy.Request(source, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)
        item = NewspapercrawlerItem()
        source = response.url
        title = sel.xpath('//h1/text()').get().strip()
        header = sel.xpath('//strong/text()').get() 
        image = 'https://jurnalul.ro/' + response.css('div.image img::attr(src)').get()
        article_body = sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "text", " " ))]')
        sentences = []

        for p in article_body.xpath('.//p/text()'):
            sentences.append(p.get())

        content = header + " ".join(str(s.strip().replace(u'\xa0', u' ')) for s in sentences)
        item['sursa'] = source
        item['titlu'] = title
        item['imagine'] = image
        item['corp'] = content
        item['rezumat'] = generate_summary(content, 2)
        yield item
