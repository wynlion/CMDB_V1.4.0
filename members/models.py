from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

# Create your models here.


class Staffs(models.Model):
    """公司职员"""

    section_type_choice = (
        # ('leaders', '领导班子'),
        ('IntegratedDepartment', '综合部'),
        ('DetectionDepartment', '检测部'),
        ('ContractDepartment', '合约部'),
        ('SecurityDepartment', '安全部'),
        ('FinanceDepartment', '财务部')
    )

    staffs_status_choice = (
        ('out', '项目'),
        ('in', '本部')
    )

    name = models.CharField(max_length=8, default='', unique=True, verbose_name='职员姓名')
    section = models.CharField(choices=section_type_choice, max_length=64, default='', verbose_name='所属部门')
    tel = models.CharField(max_length=16, default='', unique=True, verbose_name='联系方式')
    # in_or_out

    class Meta:
        verbose_name = '人事管理'
        verbose_name_plural = '人事管理'
