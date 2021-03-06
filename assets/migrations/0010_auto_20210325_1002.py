# Generated by Django 3.1.3 on 2021-03-25 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_auto_20210325_0953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idc',
            name='laboratory_status',
        ),
        migrations.AddField(
            model_name='idc',
            name='apparatus_available',
            field=models.BooleanField(default=False, verbose_name='是否可用'),
        ),
        migrations.AlterField(
            model_name='idc',
            name='apparatus_status',
            field=models.SmallIntegerField(choices=[(0, '入库'), (1, '出库'), (2, '待检'), (4, '送检'), (5, '已标定'), (6, '未知'), (7, '故障')], default=0, verbose_name='设备状态'),
        ),
    ]
