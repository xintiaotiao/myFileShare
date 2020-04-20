# Generated by Django 2.1.1 on 2018-11-06 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0002_story_for_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='sto_sort',
            field=models.CharField(default='a', max_length=32, verbose_name='排序随机字段'),
        ),
        migrations.AlterField(
            model_name='storydetail',
            name='stod_weight',
            field=models.CharField(max_length=32, verbose_name='排序'),
        ),
    ]
