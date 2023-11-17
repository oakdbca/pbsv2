# Generated by Django 4.2.7 on 2023-11-17 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("risk", "0012_risklevel_ordinal_scale_alter_likelihood_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="RiskRating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "consequence",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="risk.consequence",
                    ),
                ),
                (
                    "likelihood",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="risk.likelihood",
                    ),
                ),
            ],
        ),
    ]
