# Generated by Django 3.0.8 on 2021-10-16 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0010_auto_20211016_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='uuid',
            field=models.CharField(default='addasdasd', max_length=64),
            preserve_default=False,
        ),
    ]
