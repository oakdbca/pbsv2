# Generated by Django 4.2.6 on 2023-10-16 02:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("aviation", "0010_aviationrequest"),
    ]

    operations = [
        migrations.DeleteModel(
            name="AviationRequest",
        ),
    ]