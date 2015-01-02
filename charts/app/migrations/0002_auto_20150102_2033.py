# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chart',
            old_name='data',
            new_name='x',
        ),
        migrations.AddField(
            model_name='chart',
            name='y',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chart',
            name='dateCreated',
            field=models.DateField(default=datetime.datetime(2015, 1, 2, 20, 33, 39, 993630)),
            preserve_default=True,
        ),
    ]
