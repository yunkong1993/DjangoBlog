# Generated by Django 2.2.10 on 2020-06-01 14:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0005_auto_20200601_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userip',
            name='modified_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='最后操作时间'),
        ),
    ]