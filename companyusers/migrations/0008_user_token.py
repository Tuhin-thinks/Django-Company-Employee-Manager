# Generated by Django 4.2.4 on 2023-10-22 11:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companyusers", "0007_alter_company_funding_amt"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="token",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]