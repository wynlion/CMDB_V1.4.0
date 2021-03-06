# Generated by Django 3.0.6 on 2022-02-01 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_allprojects_member'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name': '小组成员', 'verbose_name_plural': '小组成员'},
        ),
        migrations.AlterField(
            model_name='member',
            name='belong_to_group',
            field=models.CharField(choices=[('bridge_1', '桥梁1组'), ('bridge_2', '桥梁2组'), ('bridge_petrol', '桥梁巡检组'), ('road', '道路组'), ('tunnel', '隧道组'), ('material', '材料科研组')], default='', max_length=64, verbose_name='所属小组'),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='小组成员'),
        ),
    ]
