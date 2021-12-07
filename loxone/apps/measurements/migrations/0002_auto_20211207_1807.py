# Generated by Django 3.2.9 on 2021-12-07 18:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('measurements', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='building',
            options={'default_related_name': 'buildings', 'ordering': ['name'], 'verbose_name': 'Budova', 'verbose_name_plural': 'Budovy'},
        ),
        migrations.AddField(
            model_name='building',
            name='recipients',
            field=models.ManyToManyField(null=True, related_name='buildings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='building',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Názov'),
        ),
        migrations.AlterField(
            model_name='building',
            name='password',
            field=models.CharField(max_length=500, verbose_name='Heslo'),
        ),
    ]
