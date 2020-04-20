# Generated by Django 2.1.1 on 2018-11-02 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0015_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[('0', '男'), ('1', '女')], default=1, max_length=32, verbose_name='性别'),
        ),
    ]