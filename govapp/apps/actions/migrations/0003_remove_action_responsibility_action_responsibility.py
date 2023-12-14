# Generated by Django 4.2.8 on 2023-12-14 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("actions", "0002_actionresponsibility_action_responsibility"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="action",
            name="responsibility",
        ),
        migrations.AddField(
            model_name="action",
            name="responsibility",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="actions",
                to="actions.actionresponsibility",
            ),
        ),
    ]
