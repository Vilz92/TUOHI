# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoittautuminen', '0004_auto_20151130_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='istumapaikka',
            name='omistaja',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ilmoittautuminen.Lanittaja', null=True),
        ),
    ]
