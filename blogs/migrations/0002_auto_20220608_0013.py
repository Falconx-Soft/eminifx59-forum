# Generated by Django 2.2.4 on 2022-06-07 19:13

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
