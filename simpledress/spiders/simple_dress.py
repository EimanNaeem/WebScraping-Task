from token import ISTERMINAL
import scrapy
from ..items import SimpledressItem



class DressSpider(scrapy.Spider):
    name = 'simple-dress'
    allowed_domains = ['simple-dress.com']
    start_urls = ['http://simple-dress.com/']

    def parse(self, response, **kwargs):
        for link in response.css('div.topimgtwo a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_categories)

    def parse_categories(self, response):
        for link in response.css('div.preview a::attr(href)'):
            category = response.css('div.container strong::text').get()

            yield response.follow(link.get(), callback=self.parse_products, meta={'category': category})

            next_page = response.css('div.pagination a.icon.flaticon-play45.pagination-next::attr(href)').get()
            if next_page is not None:
                link = response.urljoin(next_page)
                yield scrapy.Request(link, callback=self.parse_categories)

    def parse_products(self, response):
        category = response.meta.get('category')
        item = SimpledressItem()
        for product in response.css('div.product-view.row'):
            try:
                item ['title'] = product.css('h1.producttitle::text').get()
                item ['Image_URL'] = product.css('div.MagicToolboxContainer a::attr(href)').get()
                item ['Current_price'] : product.css('p.special-price span.price::text').get().strip().replace('$','')
                item ['old_price'] = product.css('p.old-price span.price::text').get().strip().replace('$', '')
                item ['size_options'] = product.css('div.size-custom-option option::text').getall()[2:]
                item ['Color'] = product.css('div.color-custom-option option::text').getall()[1:]
            except:
                item ['title'] = product.css('h1.producttitle::text').get()
                item ['Image_URL'] = product.css('div.MagicToolboxContainer a::attr(href)').get()
                item ['price'] = product.css('span.regular-price span.price::text').get().replace('$', '')
                item ['size_options'] = product.css('div.size-custom-option option::text').getall()[2:]
                item ['Color'] = product.css('div.color-custom-option option::text').getall()[1:]
        yield{category: item}
