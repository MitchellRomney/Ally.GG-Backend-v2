# Generated by Django 3.0.1 on 2019-12-21 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0013_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='type',
            new_name='category',
        ),
    ]