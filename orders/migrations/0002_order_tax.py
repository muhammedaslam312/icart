# Generated by Django 4.0.6 on 2022-07-27 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
