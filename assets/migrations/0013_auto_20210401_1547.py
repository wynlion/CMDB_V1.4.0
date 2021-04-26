# Generated by Django 3.1.3 on 2021-04-01 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0012_auto_20210326_1705'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logfile',
            options={'verbose_name': '文件上传', 'verbose_name_plural': '文件上传'},
        ),
        migrations.RemoveField(
            model_name='allprojects',
            name='status',
        ),
        migrations.AddField(
            model_name='allprojects',
            name='project_status',
            field=models.SmallIntegerField(choices=[(0, '开始阶段'), (1, '中期阶段'), (2, '末期阶段'), (3, '已完成'), (4, '未完成')], default=0, verbose_name='项目状态'),
        ),
        migrations.AlterField(
            model_name='logfile',
            name='file',
            field=models.FileField(upload_to='media/', verbose_name='文件'),
        ),
    ]
