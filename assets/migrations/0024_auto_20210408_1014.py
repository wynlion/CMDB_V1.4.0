# Generated by Django 3.1.3 on 2021-04-08 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0023_auto_20210407_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='belong_to',
            field=models.CharField(default='', max_length=8, verbose_name='所属部门'),
        ),
        migrations.AlterField(
            model_name='allprojects',
            name='former_status_percent',
            field=models.CharField(default='', max_length=8, verbose_name='昨日进度%'),
        ),
        migrations.AlterField(
            model_name='allprojects',
            name='project_status_percent',
            field=models.CharField(default='', max_length=8, verbose_name='项目进度%'),
        ),
    ]