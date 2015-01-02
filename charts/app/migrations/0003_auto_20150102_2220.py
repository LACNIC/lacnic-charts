# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150102_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='xTitle',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chart',
            name='yTitle',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chart',
            name='dateCreated',
            field=models.DateField(default=datetime.datetime(2015, 1, 2, 22, 20, 28, 658072)),
            preserve_default=True,
        ),
    ]
