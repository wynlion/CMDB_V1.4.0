# Generated by Django 3.1.3 on 2021-04-06 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0018_auto_20210406_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allprojects',
            name='project_status_percent',
            field=models.CharField(default='', max_length=8, verbose_name='项目进度百分比%'),
        ),
    ]
