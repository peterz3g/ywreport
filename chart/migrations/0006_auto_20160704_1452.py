# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0005_auto_20160704_1452'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itoms_count',
            old_name='crt_date1',
            new_name='crt_date',
        ),
    ]
