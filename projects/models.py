from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

# Create your models here.


class Test(models.Model):
    """测试功能"""

    test = models.CharField(max_length=64, default='', verbose_name='测试项目')

    class Meta:
        verbose_name = '测试项目'
        verbose_name_plural = '测试项目'


class AllProjects(models.Model):
    """项目总览"""

    project_type_choice = (
        ('bridge', '桥梁项目'),
        ('road', '道路项目'),
        ('experiment', '室内试验'),
        ('others', '其他项目'),
    )

    project_status_choice = (
        (0, '开始阶段'),
        (1, '中期阶段'),
        (2, '末期阶段'),
        (3, '项目结束'),
        (4, '项目暂停'),
    )

    project_type = models.CharField(choices=project_type_choice, max_length=64, default='bridge', verbose_name='项目类型')
    project_name = models.CharField(max_length=64, unique=True, default='', verbose_name='项目名称')  # 名称唯一，不可重复
    charge_person = models.CharField(max_length=64, unique=False, default='', verbose_name='项目负责人')  # 项目负责人可重复
    group_members = models.ManyToManyField('Member', blank=True, verbose_name='小组成员')
    project_status = models.SmallIntegerField(choices=project_status_choice, default=0, verbose_name='项目状态')
    project_status_percent = models.CharField(max_length=8, default='', unique=False, verbose_name='项目进度%')
    former_status_percent = models.CharField(max_length=8, default='', unique=False, verbose_name='昨日进度%')
    start_day = models.DateField(null=True, blank=True, verbose_name='项目起始日期')
    expect_finished_day = models.DateField(null=True, blank=True, verbose_name='预计完成日期')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return '<%s>' % (self.get_project_type_display())

    class Meta:
        verbose_name = '项目总览'
        verbose_name_plural = '项目总览'


class Member(models.Model):
    """成员所属"""

    section_type_choice = (
        ('detection', '检测部'),
        ('integration', '综合部'),
        ('financial', '财务部'),
        ('security', '设备安全部'),
        ('management', '经营部'),
    )

    group_type_choice = (
        ('bridge_1', '桥梁1组'),
        ('bridge_2', '桥梁2组'),
        ('bridge_petrol', '桥梁巡检组'),
        ('road', '道路组'),
        ('tunnel', '隧道组'),
        ('material', '材料科研组'),
    )

    name = models.CharField('小组成员', max_length=64, unique=True)
    belong_to_section = models.CharField(choices=section_type_choice, max_length=64, default='', verbose_name='所属部门')
    belong_to_group = models.CharField(choices=group_type_choice, max_length=64, default='', verbose_name='所属小组')
    c_day = models.DateField('创建日期', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '小组成员'
        verbose_name_plural = "小组成员"
