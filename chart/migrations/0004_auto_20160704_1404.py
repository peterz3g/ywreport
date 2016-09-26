# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0003_auto_20160704_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itoms_count',
            old_name='sys_name1',
            new_name='sys_name',
        ),
    ]
