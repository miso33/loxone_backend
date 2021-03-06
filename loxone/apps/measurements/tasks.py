import json
import logging
from uuid import uuid4
from django.conf import settings

from django.contrib.auth import get_user_model
from django.core import mail
from django.template.loader import render_to_string
from scrapyd_api import ScrapydAPI
from sentry_sdk import capture_exception

from celery import shared_task
from loxone.apps.emails.models import Email
from .models import Building, Measurement

User = get_user_model()

scrapyd = ScrapydAPI("http://localhost:6800")
logger = logging.getLogger(__name__)


@shared_task(name="scraper_previous_day")
def scraper_previous_day():
    for building in Building.objects.filter(status="active"):
        try:
            scrapyd.schedule(
                "default",
                "PreviousDayDataSpider",
                settings={
                    "unique_id": str(uuid4()),
                },
                url=building.url,
                http_user=building.login,
                http_pass=building.password,
                building=building.id,
                last_measurements=json.dumps(
                    building.measurements.last_measurements(), ensure_ascii=False
                ),
            )
        except Exception as e:
            logger.exception(e)


@shared_task(name="scraper_historical")
def scraper_historical(date_start, date_end):
    for building in Building.objects.filter(status="active"):
        try:
            task = scrapyd.schedule(
                "default",
                "HistoricalDataSpider",
                settings={
                    "unique_id": str(uuid4()),
                },
                url=building.url,
                http_user=building.login,
                http_pass=building.password,
                building=building.id,
                date_start=date_start,
                date_end=date_end,
                last_measurements=json.dumps(
                    building.measurements.last_measurements(), ensure_ascii=False
                ),
            )
            print(task)
        except Exception as e:
            logger.exception(e)


@shared_task(name="daily_report_emails")
def daily_report_emails():
    with mail.get_connection() as connection:
        for building_name, data in Measurement.objects.get_templates_data().items():
            users = list(User.objects.filter(
                is_superuser=False, is_active=True, buildings__name=building_name
            ).values_list("email", flat=True))
            if users:
                email = Email(
                    recipients=users,
                    subject=f"{building_name} - Denn?? report",
                    body_link="email.html",
                    data={"building_name": building_name, "building_data": data},
                    attempts_number=1,
                )
                email.save()
                try:
                    email_content = render_to_string(email.body_link, email.data)
                    day_report_email = mail.EmailMessage(
                        email.subject,
                        email_content,
                        settings.EMAIL_HOST_USER,
                        email.recipients,
                        connection=connection,
                    )
                    day_report_email.content_subtype = "html"
                    email.sent = day_report_email.send()
                    email.save()
                except Exception as e:
                    logger.error(e)
