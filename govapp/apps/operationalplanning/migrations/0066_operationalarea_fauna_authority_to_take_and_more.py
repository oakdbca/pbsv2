# Generated by Django 4.2.7 on 2023-12-08 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "legalapproval",
            "0009_remove_modellegalapproval_fauna_authority_to_take_and_more",
        ),
        (
            "operationalplanning",
            "0065_remove_operationalarea_requires_other_land_approval_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="operationalarea",
            name="fauna_authority_to_take",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(class)s_fauna_att",
                to="legalapproval.lawfulauthority",
                verbose_name="Fauna Authority To Take",
            ),
        ),
        migrations.AddField(
            model_name="operationalarea",
            name="flora_authority_to_take",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(class)s_flora_att",
                to="legalapproval.lawfulauthority",
                verbose_name="Flora Authority To Take",
            ),
        ),
        migrations.AddField(
            model_name="operationalplan",
            name="fauna_authority_to_take",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(class)s_fauna_att",
                to="legalapproval.lawfulauthority",
                verbose_name="Fauna Authority To Take",
            ),
        ),
        migrations.AddField(
            model_name="operationalplan",
            name="flora_authority_to_take",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(class)s_flora_att",
                to="legalapproval.lawfulauthority",
                verbose_name="Flora Authority To Take",
            ),
        ),
    ]