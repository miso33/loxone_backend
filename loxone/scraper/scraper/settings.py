import os
import sys

import django
from pathlib import Path

BOT_NAME = 'scraper'
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.append(os.path.dirname(os.path.abspath('../../apps/')))  # print (sys.path)
sys.path.append(os.path.join(BASE_DIR, "loxone_backend"))
# sys.path.append(os.path.dirname(os.path.abspath('.')))

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.base'
ITEM_PIPELINES = {
    'scraper.pipelines.MeasurementPipeline': 200,
}
django.setup()
