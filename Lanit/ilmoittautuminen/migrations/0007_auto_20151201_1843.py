# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoittautuminen', '0006_auto_20151201_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='istumapaikka',
            name='rivi',
            field=models.CharField(max_length=1),
        ),
    ]
