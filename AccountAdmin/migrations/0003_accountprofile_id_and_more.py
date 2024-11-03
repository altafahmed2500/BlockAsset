# Generated by Django 4.2.5 on 2024-10-18 18:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("AccountAdmin", "0002_remove_accountprofile_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="accountprofile",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=2,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="accountprofile",
            name="public_address",
            field=models.CharField(
                max_length=255,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Wallet address must be alphanumeric.",
                        regex="^[a-zA-Z0-9]*$",
                    )
                ],
            ),
        ),
    ]