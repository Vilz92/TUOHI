# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Istumapaikka',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('varausaika', models.DateField()),
                ('varattu_ei_maksettu', models.BooleanField(default=False)),
                ('varattu_maksettu', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Lanittaja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kokonimi', models.CharField(max_length=200)),
                ('sahkoposti', models.CharField(max_length=200)),
                ('puhnumero', models.CharField(max_length=200)),
                ('osoite', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='istumapaikka',
            name='omistaja',
            field=models.ForeignKey(to='ilmoittautuminen.Lanittaja'),
        ),
    ]
