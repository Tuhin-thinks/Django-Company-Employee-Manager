# Generated by Django 4.2.4 on 2023-10-15 18:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companyusers", "0003_company_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="slug",
            field=models.SlugField(unique=True),
        ),
    ]
