# Generated by Django 2.1.1 on 2018-11-07 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0003_auto_20181106_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='sto_sort',
            field=models.CharField(db_index=True, default='a', max_length=32, verbose_name='排序随机字段'),
        ),
    ]
