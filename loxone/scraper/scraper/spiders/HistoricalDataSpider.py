from datetime import datetime

from .BaseDataSpider import BaseDataSpider


class HistoricalDataSpider(BaseDataSpider):
    name = "HistoricalDataSpider"

    def __init__(self, *args, **kwargs):
        try:
            self.date_start = datetime.strptime(
                kwargs.get("date_start"), "%Y-%m-%d %H:%M:%S"
            )
            self.date_end = datetime.strptime(
                kwargs.get("date_end"), "%Y-%m-%d %H:%M:%S"
            )

        except Exception as e:
            self.date_start = None
            self.date_end = None
            print(e)
        self.start_of_month = None
        super().__init__(self, *args, **kwargs)

    def searching_year(self):
        return (
            self.date_start.year < self.actual_subpage.first_element_of_month.time.year
        )

    def searching_month(self):
        first_element_time = self.actual_subpage.first_element_of_month.time
        return (
            self.date_start.year == first_element_time.year
            and self.date_start.month <= first_element_time.month
        )

    def is_url_to_parse(self):
        if self.date_start and self.date_end:
            try:
                return self.searching_year() or self.searching_month()
            except Exception as e:
                print(e)
                return False
        return False

    def check_time(self, year_month, day, hour):
        return self.date_start <= datetime.strptime(
            "{0}-{1} {2:02}:00:00".format(year_month, day, hour), "%Y-%m-%d %H:%M:%S"
        )

    @staticmethod
    def not_check_time(year_month, day, hour):
        return True

    def is_end_date(self, year_month, day, hour):
        return self.date_end >= datetime.strptime(
            "{0}-{1} {2:02}:00:00".format(year_month, day, hour), "%Y-%m-%d %H:%M:%S"
        )

    def parse_url(self):
        end_of_month = self.actual_subpage.find_end_of_month()
        first_element_time = self.actual_subpage.first_element_of_month.time
        year_month = first_element_time.strftime("%Y-%m")
        time_checking = self.not_check_time
        if (
            self.date_start.year == first_element_time.year
            and self.date_start.month == first_element_time.month
        ):
            time_checking = self.check_time
        for day in range(1, int(end_of_month.time.strftime("%d")) + 1):
            for hour in range(0, 24):
                if self.is_end_date(year_month, day, hour) and time_checking(
                    year_month, day, hour
                ):
                    self.actual_subpage.find_element(year_month, day, hour)

        self.last_measurements[
            "{0} {1}".format(self.actual_subpage.zone, self.actual_subpage.type)
        ] = self.actual_subpage.last_measurement
