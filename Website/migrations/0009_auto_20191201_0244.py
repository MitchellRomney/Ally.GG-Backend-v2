# Generated by Django 2.2.6 on 2019-12-01 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Website', '0008_auto_20191109_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='main_summoner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Main_Summoners', to='Website.Summoner'),
        ),
        migrations.CreateModel(
            name='RegistrationInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='RegistrationInterest_User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
