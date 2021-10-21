from datetime import datetime

import scrapy
from lxml import etree
from time import strftime
from ..items import MeasurementItem


# from scrapy_django_dashboard.spiders.django_spider import DjangoSpider


class StatsSpider(scrapy.Spider):
    name = "StatsSpider"
    # start_urls = ["http://www.komenskehocollege.sk/"]
    # # http_user = "admin",
    # # http_pass = "Stefanikova-22",
    http_user = 'labas'
    http_pass = 'Lx20-10KE*'
    start_urls = [
        'http://85.237.251.24:10510/stats/'
    ]

    # def __init__(self, *args, **kwargs):
    #     # self.url = kwargs.get('url')
    #     # self.domain = kwargs.get('domain')
    #     print(kwargs.get('start_urls'))
    #     print("nieco")
    #     self.start_urls = [kwargs.get('start_urls')]
    #
    #     super(StatsSpider, self).__init__(*args, **kwargs)

    #
    # def __init__(self, *args, **kwargs):
    #     # print("tus")
    #     #
    #     # self.http_user = kwargs.get('http_user')
    #     # self.http_pass = kwargs.get('http_pass')
    #     self.start_urls = [kwargs.get('url')]

    def datetime_to_year_month(self, tree):
        return datetime.strptime(tree.attrib['T'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')

    def actual_month(self, first_date, second_date):
        today = strftime("%Y-%m")
        if today == self.datetime_to_year_month(first_date) or today == self.datetime_to_year_month(second_date):
            return True
        return False

    def parse(self, response):
        pages = response.css('li a::attr(href)').getall()
        pages.reverse()
        if pages:
            for string in pages:
                try:
                    yield scrapy.Request(response.request.url + string, callback=self.parse)
                except:
                    pass
        else:
            parser = etree.XMLParser(recover=True)
            tree = etree.fromstring(response.body, parser=parser)
            type = "T" if tree.attrib['Name'].split(" ")[0] == 'Teplota' else "H"
            zone = tree.attrib['Outputs']
            url = response.request.url.split("/")[-1]
            if self.actual_month(tree[0], tree[1]):
                measurements = []
                for idx, child in enumerate(tree):
                    try:
                        yield {
                            'time': datetime.strptime(child.attrib['T'], '%Y-%m-%d %H:%M:%S').strftime(
                                '%Y-%m-%d %H:%M:%S'),
                            'value': float("{:.1f}".format(float(child.attrib['V']))),
                            'zone': zone,
                            'type': type,
                            'url': url,
                            'building': 1,
                        }
                        # measurement_data = {
                        #     'date': datetime.strptime(child.attrib['T'], '%Y-%m-%d %H:%M:%S').strftime(
                        #         '%Y-%m-%d %H:%M:%S'),
                        #     'value': val,
                        #     'zone': zone,
                        #     'type': type,
                        #     'url': url,
                        # }
                        # print(measurement_data)
                    except:
                        pass
                        # print("error")
                # print(measurements)
                # print(measurements)
                # yield measurements
