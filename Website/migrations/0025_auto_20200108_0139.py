# Generated by Django 3.0.1 on 2020-01-08 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0024_auto_20200108_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='promotion_division',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
