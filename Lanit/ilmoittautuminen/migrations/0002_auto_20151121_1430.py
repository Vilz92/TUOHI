# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoittautuminen', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='istumapaikka',
            old_name='varattu_ei_maksettu',
            new_name='maksettu',
        ),
        migrations.RenameField(
            model_name='istumapaikka',
            old_name='varattu_maksettu',
            new_name='varattu',
        ),
    ]
