import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.vagrant')
app = Celery('proj')
app.conf.broker_url = 'redis://localhost:6379/0'
app.autodiscover_tasks(settings.INSTALLED_APPS)
task = app.task

#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, task.fun2.s('hello'), name='add every 10')
#     # sender.add_periodic_task(10.0, fun2.s('hello'), name='add every 10')
# #
# #     # # Executes every Monday morning at 7:30 a.m.
# #     # sender.add_periodic_task(
# #     #     crontab(hour=7, minute=30, day_of_week=1),
# #     #     test.s('Happy Mondays!'),
# #     # )

# app.conf.beat_schedule = {
#     #Scheduler Name
#     'buildings-scraper': {
#         # Task Name (Name Specified in Decorator)
#         'task': 'buildings-scraper',
#         # Schedule
#         # 'schedule':  crontab(minute=55, hour=8),
#         'schedule': 120.00,
#
#         # Function Arguments
#         'args': ("Hello",)
#     },
# }
