# Generated by Django 4.0.6 on 2022-07-22 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_variation_variation_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_value',
            field=models.CharField(max_length=100),
        ),
    ]
