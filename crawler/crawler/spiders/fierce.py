import scrapy
import json

class FierceSpider(scrapy.Spider):
    name = "fierce"
    start_urls = ["https://www.fiercebiotech.com/devices"]

    def parse(self, response):

        # 抓 JSON-LD
        scripts = response.css('script[type="application/ld+json"]::text').getall()

        for script in scripts:
            try:
                data = json.loads(script)

                # 確保是文章列表
                if data.get("@type") == "ItemList":
                    items = data.get("itemListElement", [])

                    for item in items:
                        article = item.get("item", {})

                        yield {
                            "title": article.get("name"),
                            "url": article.get("url"),
                            "description": article.get("description"),
                        }

            except Exception as e:
                continue