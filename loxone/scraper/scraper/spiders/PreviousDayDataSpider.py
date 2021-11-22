from datetime import datetime
from datetime import date, timedelta
from .BaseDataSpider import BaseDataSpider


class PreviousDayDataSpider(BaseDataSpider):
    name = "PreviousDayDataSpider"

    def __init__(self, *args, **kwargs):
        print("Tu som ja 2")
        super().__init__(self, *args, **kwargs)

    def is_url_to_parse(self):
        print("HOVNO2")
        try:
            return datetime.today().strftime(
                "%Y-%m"
            ) == self.actual_subpage.first_element_of_month.time.strftime("%Y-%m")
        except Exception as e:
            print(e)
            return False

    def parse_url(self):
        first_element_time = self.actual_subpage.first_element_of_month.time
        year_month = first_element_time.strftime("%Y-%m")
        yesterday = int((date.today() - timedelta(days=1)).strftime("%d"))
        for hour in range(0, 24):
            print("tu som")
            self.actual_subpage.find_element(year_month, yesterday, hour)
