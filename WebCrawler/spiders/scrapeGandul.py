import scrapy
from WebCrawler.items import NewspapercrawlerItem
from scrapy.selector import Selector
from Extensie.summarizer import generate_summary 

class ScrapeGandul(scrapy.Spider):
    name = "gandul"
    base_url = "https://www.gandul.ro/ultima-ora/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    def start_requests(self):
        for page in range(1, 11):
            page_url = self.base_url + 'page/' + str(page)
            print(page_url)
            yield scrapy.Request(url = page_url, headers = self.headers, callback = self.parse)

    def parse(self, response):
        sel = Selector(response) 
        article_headers = sel.xpath('//*[(@id = "main")]//a')
        for header in article_headers:
            source = header.xpath('@href').extract()[0]
            print(source)
            yield scrapy.Request(source, callback=self.parse_article)

    def parse_article(self, response):
        sel = Selector(response)
        item = NewspapercrawlerItem()
        source = response.url
        header = sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "single__content", " " ))]//strong/text()').get()
        title = response.css('h1[class="font-titles"]::text').get()
        image = response.css('div.single__media img::attr(src)').get()
        article_body = sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "single__content", " " ))]')
        sentences = []

        for p in article_body.xpath('.//p/text()'):
            sentences.append(p.get())

        content =  header + " ".join(str(s.strip().replace(u'\xa0', u' ')) for s in sentences)
        item['sursa'] = source
        item['titlu'] = title
        item['imagine'] = image
        item['corp'] = content
        item['rezumat'] = generate_summary(content, 2)
        yield item

