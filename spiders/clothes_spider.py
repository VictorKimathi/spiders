import scrapy

class ClothesSpider(scrapy.Spider):
    name = "clothes"
    start_urls = [
        "https://www.amazon.com/s?k=clothes&crid=1T8H6K3ATDTF2&sprefix=clothes%2Caps%2C317&ref=nb_sb_noss_1"
    ]

    def parse(self, response):
        # Extract the image URLs
        image_urls = response.css('img.s-image::attr(src)').getall()[1:]
        
        # Extract the product names
        product_names = response.css('h2.a-size-mini a span.a-size-base-plus::text').getall()
        
        # Extract the prices
        prices = response.css('span.a-price span.a-offscreen::text').getall()
        
        # Extract the delivery times
        delivery_times = response.css('div[data-cy="delivery-recipe"] span.a-color-base.a-text-bold::text').getall()
        
        # Collect all these into a list of dictionaries
        for img, name, price, delivery in zip(image_urls, product_names, prices, delivery_times):
            yield {
                'image_url': img,
                'name': name,
                'price': price,
                'delivery_time': delivery
            }
