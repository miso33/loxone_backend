from .Element import Element, EmptyElement


class SubPage:
    def __init__(self, tree, url, building, last_measurements):
        try:
            self.tree = tree
            self.zone = self.set_zone()
            self.type = self.set_type()
            self.children = tree.findall("S")
            self.first_element_of_month = self.find_first_element_of_month()
            self.url = url
            self.measurements_to_yield = []
            self.building = building
            self.last_measurement = self.set_last_measurements(last_measurements)
        except Exception:
            self.tree = None

    def check_type_string(self, type_string):
        return bool(
            [word for word in type_string if (word in self.tree.attrib["Name"].lower())]
        )

    def set_type(self):
        try:
            if self.check_type_string(["teplota"]):
                return "temperature"
            if self.check_type_string(["vlhkost", "vlhkosť", "vzduchu"]):
                return "humidity"
            if self.check_type_string(["co2"]):
                return "CO2"
            return "unknown"
        except Exception as e:
            print(e)
            return self.type

    def set_zone(self):
        try:
            return self.tree.attrib["Outputs"]
        except Exception:
            return None

    def set_last_measurements(self, last_measurements):
        try:
            return (
                last_measurements["{0} {1}".format(self.zone, self.type)]
                if "{0} {1}".format(self.zone, self.type) in last_measurements
                else 0
            )
        except Exception:
            return 0

    def compare_first_with_second_element(self):
        try:
            first_element = Element(self.children[0])
            second_element = Element(self.children[1])
            if first_element.time.month == second_element.time.month:
                return first_element
            return second_element
        except Exception:
            return None

    def find_first_element_of_month(self):
        try:
            if self.children:
                if len(self.children) > 1:
                    return self.compare_first_with_second_element()
                return Element(self.children[0])
        except Exception:
            return None

    def find_end_of_month(self):
        try:
            counter = -1
            end_of_month = Element(self.children[counter])
            while end_of_month.time.month != self.first_element_of_month.time.month:
                counter -= 1
                end_of_month = Element(self.children[counter])
            return end_of_month
        except Exception:
            return False

    def create_measurement(self, element):
        return {
            "time": element.time.strftime("%Y-%m-%d %H:%M:%S"),
            "value": float("{:.1f}".format(round(float(element.value), 2))),
            "zone": self.zone,
            "type": self.type,
            "url": self.url,
            "building": self.building,
        }

    def find_element(self, year_month, day, hour):
        try:
            time = "{0}-{1:02} {2:02}:00:00".format(year_month, day, hour)
            element_found = self.tree.xpath("//S[@T='{0}']".format(time))
            if element_found:
                element = Element(element_found[0])
                self.last_measurement = element.value
            else:
                element = EmptyElement(time=time, value=self.last_measurement)
            self.measurements_to_yield.append(self.create_measurement(element))
        except Exception as e:
            print(e)
