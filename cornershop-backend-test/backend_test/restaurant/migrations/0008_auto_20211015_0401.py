# Generated by Django 3.0.8 on 2021-10-15 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_auto_20211015_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comments',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='date',
            field=models.DateField(),
        ),
    ]
