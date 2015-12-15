# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoittautuminen', '0002_auto_20151121_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lanittaja',
            name='sahkoposti',
            field=models.EmailField(max_length=254),
        ),
    ]
