# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoittautuminen', '0005_auto_20151130_0044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='istumapaikka',
            old_name='x',
            new_name='paikkanumero',
        ),
        migrations.RenameField(
            model_name='istumapaikka',
            old_name='y',
            new_name='rivi',
        ),
    ]
