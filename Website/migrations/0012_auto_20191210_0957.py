# Generated by Django 2.2.6 on 2019-12-10 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0011_profile_third_party_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='third_party_token',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
