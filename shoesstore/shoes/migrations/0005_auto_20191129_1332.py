# Generated by Django 2.2.6 on 2019-11-29 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0004_auto_20191129_1307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='name',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]