# Generated by Django 3.2.9 on 2021-12-07 18:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('measurements', '0002_auto_20211207_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='recipients',
            field=models.ManyToManyField(related_name='buildings', to=settings.AUTH_USER_MODEL),
        ),
    ]
