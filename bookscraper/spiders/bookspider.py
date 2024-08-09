

import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        
        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            book_url = response.urljoin(relative_url)
            
            yield response.follow(book_url, callback=self.parse_book_page)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        table_rows = response.css('table tr')
        
        yield {
            'url': response.url,
            'title': response.css('.product_page div h1::text').get(),
            'product_type': table_rows[1].css('td::text').get(),
            'price_exl_tax': table_rows[2].css('td::text').get(),
            'price_incl_tax': table_rows[3].css('td::text').get(),
            'tax': table_rows[4].css('td::text').get(),
            'category': response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price': response.css('p.price_color::text').get(),
        }
