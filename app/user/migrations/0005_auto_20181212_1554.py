# Generated by Django 2.1.3 on 2018-12-12 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20181212_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='联系电话'),
        ),
    ]
