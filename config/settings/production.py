from .celery import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import mimetypes

DEBUG = False

mimetypes.add_type("text/css", ".css", True)

sentry_sdk.init(
    dsn="https://a5797ef14d444ec7ba5336b507a778f8@o1085724.ingest.sentry.io/6097334",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
SERVER_EMAIL = env("EMAIL_HOST_USER")

ADMINS = [("admin", "reports@scrypta.sk")]
