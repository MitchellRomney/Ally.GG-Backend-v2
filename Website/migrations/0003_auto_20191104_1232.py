# Generated by Django 2.2.6 on 2019-11-04 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0002_champion_item_match_participant_rune_summonerspell_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner',
            name='summoner_level',
            field=models.IntegerField(blank=True),
        ),
    ]
