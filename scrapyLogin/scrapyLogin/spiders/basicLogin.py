from scrapy.http import FormRequest
import scrapy


class BasicloginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["quotes.toscrape.com"]
    url_base = "http://quotes.toscrape.com"
    custom_settings = {
        "FEED_URI": "quotes.json",
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    def start_requests(self):
        login_url = "http://quotes.toscrape.com/login"
        yield scrapy.Request(login_url, callback=self.login)

    def login(self, response):
        token = response.css("form input[name=csrf_token]::attr(value)").extract_first()
        yield FormRequest.from_response(
            response,
            formdata={"csrf_token": token, "username": "adavid", "password": "12345"},
            callback=self.parse,
        )

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "author": quote.css("small.author::text").get(),
                "phrase": quote.css("span.text::text").get(),
            }

        next = response.css(".next > a::attr(href)").get()
        if next:
            next_url = self.url_base + next
            yield scrapy.Request(next_url, callback=self.parse)
