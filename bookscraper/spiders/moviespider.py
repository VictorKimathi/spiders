import scrapy


class MoviespiderSpider(scrapy.Spider):
    name = "moviespider"
    allowed_domains = ["https://nkiri.com/tv-series-list"]
    start_urls = ["https://nkiri.com/tv-series-list"]

    def parse(self, response):
        pass
        movies = response.css('article.eael-grid-post')
        for movie in movies:
            # relative_url = movie.css('h3 a::attr(href)').get()
            movie_url =  response.css("div.elementor-button-wrapper a::attr(href)").get()
            if movie_url:
                yield response.follow(movie_url, callback=self.parse_movie_page)

        next_page = response.css("div.elementor-button-link a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_movie_page(self, response):
        # table_rows = response.css('table tr')
        
        yield {
            'image':response.css('article.eael-grid-post img.attachment-medium::attr(src)').get(),
            'title': response.css('h6.eael-entry-title ::text').get(),
            'link':  response.css('a.eael-grid-post-link  ::attr(href)').get(),
            'date': response.css('div.eael-entry-meta span  time ::text').get(),
      
        }
# import scrapy

# class MoviespiderSpider(scrapy.Spider):
#     name = "moviespider"
#     allowed_domains = ["nkiri.com"]
#     start_urls = ["https://nkiri.com/tv-series-list/"]


#     def parse(self, response):
#         self.logger.info(response.text)  # Log the response body for debugging
#         for movie in response.css('.info-column a::attr(href)'):
#             movie_url = movie.get()
#             if movie_url:
#                 self.logger.info(f'Movie URL: {movie_url}')
#                 yield {'movie_url': movie_url}
#             else:
#                 self.logger.info('Movie URL: None')


#         # Handling pagination
#         next_page = response.css("a.page-numbers.next::attr(href)").get()
#         if next_page:
#             print(f"Next page: {next_page}")
#             yield response.follow(next_page, callback=self.parse)

#     def parse_movie_page(self, response):
#         # Extracting data from the movie page
#         yield {
#             'image': response.css('img.attachment-medium::attr(src)').get(),
#             'title': response.css('h1.entry-title::text').get(),
#             'link': response.url,
#             'date': response.css('time.entry-date::attr(datetime)').get(),
#         }
