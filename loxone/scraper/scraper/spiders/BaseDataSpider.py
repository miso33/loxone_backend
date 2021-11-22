import json

import scrapy

from lxml import etree

from .SubPage import SubPage


class BaseDataSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        try:
            self.start_urls = [kwargs.get("url")]
            self.http_user = kwargs.get("http_user")
            self.http_pass = kwargs.get("http_pass")
            self.building = kwargs.get("building")
            self.actual_subpage = None
            self.last_measurements = (
                json.loads(kwargs.get("last_measurements"))
                if kwargs.get("last_measurements")
                else {}
            )
        except Exception as e:
            print(e)

    def is_url_to_parse(self):
        return False

    def parse_url(self):
        pass

    def parse(self, response):
        try:
            pages = response.css("li a::attr(href)").getall()
            pages.reverse()
            if pages:
                for string in pages:
                    try:
                        yield scrapy.Request(
                            response.request.url + string, callback=self.parse
                        )
                    except Exception as e:
                        print(e)
            else:
                parser = etree.XMLParser(recover=True)
                self.actual_subpage = SubPage(
                    tree=etree.fromstring(response.body, parser=parser),
                    url=response.request.url.split("/")[-1],
                    building=self.building,
                    last_measurements=self.last_measurements,
                )
                if self.is_url_to_parse():
                    self.parse_url()
                    for measurement in self.actual_subpage.measurements_to_yield:
                        yield measurement
        except Exception as e:
            print(e)
