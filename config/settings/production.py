from .celery import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False


sentry_sdk.init(
    dsn="https://0e373a22cb4446f1b9b7c65033467e5b@o1070615.ingest.sentry.io/6066737",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
