# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150102_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='dateCreated',
            field=models.DateField(default=datetime.datetime(2015, 4, 8, 19, 33, 6, 527793)),
        ),
    ]
