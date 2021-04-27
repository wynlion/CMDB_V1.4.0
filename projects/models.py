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

