# Generated by Django 4.2.4 on 2023-10-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "companyusers",
            "0002_user_address1_user_address2_user_city_user_country_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="slug",
            field=models.SlugField(default="no-slug"),
        ),
    ]