# Generated by Django 2.2.4 on 2022-06-10 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0010_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]