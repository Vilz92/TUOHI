# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoittautuminen', '0003_auto_20151129_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='istumapaikka',
            name='varausaika',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='lanittaja',
            name='puhnumero',
            field=models.CharField(max_length=20),
        ),
    ]
