from django.shortcuts import render
from projects import models
from CMDB import settings

# Create your views here.


def allprojects(request):
    """
    项目总览示意图
    :param request:
    :return:
    """
    projects = models.AllProjects.objects.all()
    return render(request, 'projects/allprojects.html', locals())
