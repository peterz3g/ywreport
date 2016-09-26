# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0006_auto_20160704_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itoms_count',
            name='sys_name',
            field=models.CharField(default=b'itoms', max_length=256, db_index=True),
        ),
        migrations.AlterIndexTogether(
            name='itoms_count',
            index_together=set([('crt_date', 'itoms_type')]),
        ),
    ]
