import scrapy


class VergeSpider(scrapy.Spider):
    name = 'VergeCrawlr'
    allowed_domains = ['theverge.com']

    def start_requests(self):
        urls = [
            'https://www.theverge.com/reviews/'
        ]
        return [scrapy.Request(url=url, callback=self.parse) for url in urls]

    def parse(self, response):
        url = response.url
        title = response.css('h1::text').extract_first()
        author = response.css('span.c-byline__author-name::text').extract_first()
        author_link = response.css('span.c-byline__item a::attr(href)').extract_first()

        review = VergeReview()

        self.log('URL :: {} '.format(url))
        review['url'] = url
        self.log('TITLE :: {} '.format(title))
        review['title'] = title
        self.log('AUTHOR :: {} '.format(author))
        review['author'] = author
        self.log('AUTHOR-LINK :: {} '.format(author_link))
        review['author_link'] = author_link

        self.log('')

        yield review

        for href in response.xpath("//div[@class='c-entry-box--compact__body']/h2/a/@href").extract():
            if not str(href).__contains__('mailto:'):
                self.log(href)
                yield response.follow(response.urljoin(href), callback=self.parse)


class VergeReview(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    author_link = scrapy.Field()
