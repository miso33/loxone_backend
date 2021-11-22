from datetime import datetime


class Element:
    def __init__(self, element):
        try:
            self.datetime_format = "%Y-%m-%d %H:%M:%S"
            self.time = self.element_to_datetime(element)
            self.value = self.find_value(element)
        except Exception as e:
            self.datetime_format = "%Y-%m-%d %H:%M:%S"
            self.time = None
            self.value = None

    def string_to_datetime(self, string):
        return datetime.strptime(string, self.datetime_format)

    def element_to_datetime(self, element):
        return (
            self.string_to_datetime(element.attrib["T"])
            if "T" in element.attrib
            else None
        )

    def find_value(self, element):
        return element.attrib["V"]


class EmptyElement:
    def __init__(self, time, value):
        try:
            self.time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            self.value = value
        except Exception as e:
            print(e)
            self.time = None
            self.value = None
