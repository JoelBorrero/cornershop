# Generated by Django 3.0.8 on 2021-10-16 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0009_order_menu'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='comments',
            new_name='observations',
        ),
    ]
