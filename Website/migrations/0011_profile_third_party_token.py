# Generated by Django 2.2.6 on 2019-12-02 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0010_accesscode'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='third_party_token',
            field=models.CharField(default='None', max_length=12),
            preserve_default=False,
        ),
    ]
