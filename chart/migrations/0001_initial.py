# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='itoms_count1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crt_date', models.CharField(default=b'20160101', max_length=16)),
                ('itoms_type', models.CharField(default=b'itoms', max_length=256)),
                ('sys_name', models.CharField(default=b'itoms', max_length=256)),
                ('itoms_status', models.CharField(default=b'itoms', max_length=256)),
                ('count', models.IntegerField(default=1)),
            ],
        ),
    ]
