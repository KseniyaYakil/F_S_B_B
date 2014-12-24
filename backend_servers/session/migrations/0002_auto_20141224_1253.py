# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionauth',
            name='cookie_token',
            field=models.CharField(unique=True, max_length=1024),
            preserve_default=True,
        ),
    ]
