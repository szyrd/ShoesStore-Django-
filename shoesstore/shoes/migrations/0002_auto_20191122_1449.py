# Generated by Django 2.2.6 on 2019-11-22 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female')], default='m', max_length=2),
        ),
    ]
