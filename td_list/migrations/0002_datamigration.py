# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from ..list_data import list_data


def forwards_func(apps, schema_editor):
    for label_lower, names in list_data.items():
        model = apps.get_model(*label_lower.split('.'))
        db_alias = schema_editor.connection.alias
        for index, name in enumerate(names):
            model.objects.using(db_alias).create(name=name, short_name=name, display_index=index)


def reverse_func(apps, schema_editor):
    for label_lower, names in list_data.items():
        model = apps.get_model(*label_lower.split('.'))
        db_alias = schema_editor.connection.alias
        for name in names:
            model.objects.using(db_alias).filter(name=name).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('td_list', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
