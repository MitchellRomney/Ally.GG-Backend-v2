# Generated by Django 3.0.1 on 2019-12-29 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0018_auto_20191226_0854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrationinterest',
            old_name='first_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='postinteraction',
            name='post_interaction_type',
            field=models.IntegerField(choices=[(1, 'LIKE'), (2, 'UNLIKED')]),
        ),
    ]
