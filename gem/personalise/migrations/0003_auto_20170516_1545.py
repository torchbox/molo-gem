# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-16 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalise', '0002_auto_20170516_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiledatarule',
            name='operator',
            field=models.CharField(choices=[(b'lt', 'Less than'), (b'lte', 'Less than or equal'), (b'gt', 'Greater than'), (b'gte', 'Greater than or equal'), (b'eq', 'Equal'), (b'neq', 'Not equal'), (b'reg', 'Regex')], default='eq', max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profiledatarule',
            name='field',
            field=models.CharField(choices=[(b'user__date_joined', b'User - Date Joined'), (b'userprofile__date_of_birth', b'User Profile - Date Of Birth'), (b'gemuserprofile__gender', b'Gem User Profile - Gender')], max_length=255),
        ),
    ]
