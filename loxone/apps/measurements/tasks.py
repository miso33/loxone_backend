from celery import shared_task
from loxone.apps.buildings.models import Building
from scrapyd_api import ScrapydAPI

scrapyd = ScrapydAPI('http://localhost:6800')


@shared_task(name='buildings-scraper')
def buildings_scraper():
    # building = Building.objects.first()
    settings = {
        'unique_id': "5",
        # 'http_user':"labas",
        # 'http_pass':building.password,
    }
    task = scrapyd.schedule('default', 'StatsSpider',
                            settings=settings)
