"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
# Generated by Django 3.1.4 on 2021-03-04 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_squashed_0065_auto_20210223_2014"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="project",
            unique_together=set(),
        ),
    ]
