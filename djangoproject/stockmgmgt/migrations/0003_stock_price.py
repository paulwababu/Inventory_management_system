# Generated by Django 3.0.8 on 2020-08-08 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmgt', '0002_stockhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='price',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
    ]
