# Generated by Django 2.1.1 on 2018-11-03 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stoKind',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sto_kind', models.CharField(max_length=32, unique=True, verbose_name='文学分类名')),
                ('ctime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '文学分类表管理',
            },
        ),
        migrations.CreateModel(
            name='story',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sto_name', models.CharField(max_length=32, verbose_name='文章名称')),
                ('sto_img', models.ImageField(max_length=128, upload_to='static/upload/%Y-%m-%d/', verbose_name='图片地址')),
                ('sto_intro', models.TextField(verbose_name='文章简介')),
                ('sto_hot', models.IntegerField(verbose_name='点击量')),
                ('sto_weight', models.IntegerField(verbose_name='文章排序')),
                ('sto_use', models.IntegerField(choices=[(0, '上线'), (1, '下线')], verbose_name='是否上线')),
                ('ctime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('for_kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='story.stoKind', verbose_name='所属类别')),
            ],
            options={
                'verbose_name_plural': '文学栏目表管理',
            },
        ),
        migrations.CreateModel(
            name='storyDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stod_title', models.CharField(max_length=32, verbose_name='文章标题')),
                ('stod_content', models.TextField(verbose_name='文章内容')),
                ('stod_weight', models.IntegerField(unique=True, verbose_name='文章排序')),
                ('stod_use', models.IntegerField(choices=[(0, '上线'), (1, '下线')], verbose_name='是否上线')),
                ('ctime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('for_story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='story.story', verbose_name='所属文章')),
            ],
            options={
                'verbose_name_plural': '文学栏目详情表管理',
            },
        ),
    ]
