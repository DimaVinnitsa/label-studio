# Generated by Django 3.1.4 on 2021-03-14 18:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0007_auto_20210309_1304"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="sampling",
            field=models.CharField(
                choices=[
                    ("Sequential sampling", "Tasks are ordered by their IDs"),
                    ("Uniform sampling", "Tasks are chosen randomly"),
                    (
                        "Uncertainty sampling",
                        "Tasks are chosen according to model uncertainty scores (active learning mode)",
                    ),
                ],
                default="Sequential sampling",
                max_length=100,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="title",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Project name. Must be between 3 and 50 characters long.",
                max_length=50,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(3),
                    django.core.validators.MaxLengthValidator(50),
                ],
                verbose_name="title",
            ),
        ),
    ]
