# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0007_auto_20160704_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='itoms_count',
            name='area_name',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='itoms_count',
            name='sys_name',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
