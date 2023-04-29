from pathlib import Path

import scrapy


class SaasWorthy(scrapy.Spider):
    name = "saas_worthy"

    def start_requests(self):
        urls = [
            "https://www.saasworthy.com/list",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_category_list)

    def parse_category_list(self, response):
        links = response.xpath("//a[starts-with(@href, '/list/')]")
        yield from response.follow_all(links, callback=self.parse_category_page)

    def parse_category_page(self, response):
        product_links = response.xpath("//p[@class='pro-desc-question']/a")
        yield from response.follow_all(product_links, callback=self.parse_product_page)

        links = response.xpath("//a[starts-with(@id, 'email-marketing-software-href-')]")
        yield from response.follow_all(links, callback=self.parse_category_page)

    def parse_product_page(self, response):
        description = response.xpath("//meta[@property='og:description']/@content").get()
        if description:
            yield {
                "description": description,
                "name": response.xpath("//h1[@class='h-title']/text()").get(),
                "url": response.url
            }
