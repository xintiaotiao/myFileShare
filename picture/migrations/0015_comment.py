# Generated by Django 2.1.1 on 2018-11-01 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0014_remove_pic_pic_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('com_ip', models.GenericIPAddressField(default='127.0.0.1', verbose_name='评论者IP')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('from_pic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picture.Pic', verbose_name='所属相册')),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='picture.User', verbose_name='评论者')),
            ],
            options={
                'verbose_name_plural': '相册评论表',
            },
        ),
    ]
