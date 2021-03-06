# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-08 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0008_auto_20160706_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='itoms_chg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crt_date', models.CharField(default=b'20160101', max_length=16)),
                ('itoms_type', models.CharField(default=b'itoms', max_length=256)),
                ('sys_name', models.CharField(max_length=256, null=True)),
                ('area_name', models.CharField(max_length=256, null=True)),
                ('itoms_status', models.CharField(default=b'itoms', max_length=256)),
                ('emergency_reason', models.CharField(default=b'', max_length=256)),
                ('count', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='itoms_para_mod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crt_date', models.CharField(default=b'20160101', max_length=16)),
                ('itoms_type', models.CharField(default=b'itoms', max_length=256)),
                ('sys_name', models.CharField(max_length=256, null=True)),
                ('mod_type', models.CharField(max_length=256, null=True)),
                ('itoms_status', models.CharField(default=b'itoms', max_length=256)),
                ('mod_reason', models.CharField(default=b'', max_length=256)),
                ('count', models.IntegerField(default=1)),
            ],
        ),
        migrations.AlterIndexTogether(
            name='itoms_para_mod',
            index_together=set([('crt_date',)]),
        ),
        migrations.AlterIndexTogether(
            name='itoms_chg',
            index_together=set([('crt_date',)]),
        ),
    ]
