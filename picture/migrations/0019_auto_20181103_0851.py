# Generated by Django 2.1.1 on 2018-11-03 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0018_auto_20181103_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_log',
            field=models.IntegerField(choices=[(1, '上线'), (2, '下线')], default=2, verbose_name='是否开启'),
        ),
    ]
