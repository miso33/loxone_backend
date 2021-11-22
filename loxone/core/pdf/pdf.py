import pdfkit
from django.conf import settings


class Pdf:
    def __init__(self):
        self.config = None
        if settings.WKHTMLTOPDF_PATH:
            self.config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)

    def generate(self, template, options):
        return pdfkit.from_string(
            template, False, configuration=self.config, options=options
        )
