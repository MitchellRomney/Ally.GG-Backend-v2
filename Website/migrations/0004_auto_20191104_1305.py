# Generated by Django 2.2.6 on 2019-11-04 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0003_auto_20191104_1232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participant',
            old_name='positions',
            new_name='position',
        ),
    ]
