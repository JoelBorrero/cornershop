# Generated by Django 3.0.8 on 2021-10-15 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_remove_employee_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='description',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='meals',
        ),
        migrations.CreateModel(
            name='Combination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('meals', models.ManyToManyField(to='restaurant.Meal')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='options',
            field=models.ManyToManyField(to='restaurant.Combination'),
        ),
    ]
