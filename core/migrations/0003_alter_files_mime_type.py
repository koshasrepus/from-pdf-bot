# Generated by Django 3.2.2 on 2021-06-15 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_files_mime_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='mime_type',
            field=models.CharField(max_length=96),
        ),
    ]
