# Generated by Django 4.2.11 on 2024-03-08 03:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("actions", "0005_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="actionresponsibility",
            options={
                "verbose_name": "Action Responsibility",
                "verbose_name_plural": "Action Responsibilities",
            },
        ),
    ]