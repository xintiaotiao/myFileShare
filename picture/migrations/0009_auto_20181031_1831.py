# Generated by Django 2.1.1 on 2018-10-31 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0008_auto_20181031_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic',
            name='pic_weight',
            field=models.CharField(default=1, max_length=32, verbose_name='权重'),
        ),
        migrations.AlterField(
            model_name='picdetail',
            name='picd_weight',
            field=models.CharField(default=1, max_length=32, verbose_name='图片权重'),
        ),
    ]
