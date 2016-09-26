# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0002_auto_20160704_1352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itoms_count',
            old_name='sys_name',
            new_name='sys_name1',
        ),
    ]
