import scrapy
from WebCrawler.items import NewspapercrawlerItem
from scrapy.selector import Selector 
from Extensie.summarizer import generate_summary 

class ScrapeLibertatea(scrapy.Spider):
    name = "libertatea"
    base_url = "https://www.libertatea.ro/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    def start_requests(self):
        yield scrapy.Request(url = self.base_url, headers = self.headers, callback = self.parse)


    def parse(self, response):

        sel = Selector(response)
        article_headers = sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "article-title", " " ))]//a')

        for header in article_headers:
            source = header.xpath('@href').extract()[0]
            yield scrapy.Request(source, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)
        item = NewspapercrawlerItem()
        source = response.url 
        title = sel.xpath('//h1/text()').get()
        image = response.css('div.thumb .img-responsive::attr(src)').get()
        header = response.css('p[class="intro"]::text').get()
        article_body = sel.xpath('/html/body/section[3]/div/div[1]/div[2]/div')
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

