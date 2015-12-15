# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoittautuminen', '0007_auto_20151201_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='istumapaikka',
            name='varausaika',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
