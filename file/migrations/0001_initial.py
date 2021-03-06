# Generated by Django 2.1.1 on 2018-11-08 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=32, verbose_name='文件名')),
                ('file_path', models.FileField(max_length=128, upload_to='static/upload/%Y-%m-%d/', verbose_name='下载地址')),
                ('file_size', models.CharField(default='null', max_length=32, verbose_name='文件大小')),
                ('file_ip', models.CharField(default='127.0.0.1', max_length=32, verbose_name='上传者')),
                ('file_hot', models.IntegerField(default=1, verbose_name='点击量')),
                ('file_intro', models.TextField(default='作者：心跳跳', max_length=64, verbose_name='文件介绍')),
                ('file_time', models.DateField(auto_now_add=True, verbose_name='上传时间')),
            ],
            options={
                'verbose_name_plural': '文件表',
            },
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='分类名称')),
                ('ctime', models.DateField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '文件分类表',
            },
        ),
        migrations.AddField(
            model_name='file',
            name='file_kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file.Kind', verbose_name='文件类别'),
        ),
    ]
