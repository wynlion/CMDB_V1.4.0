from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Function(models.Model):
    """新增功能区"""

    function = models.CharField(max_length=64, default='', verbose_name='新增功能')

    class Meta:
        verbose_name = '新增功能'
        verbose_name_plural = '新增功能'
