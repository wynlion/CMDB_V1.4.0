from django.db import models
from django.test import TestCase
from assets.models import ReportLists

# Create your tests here.
raw_dict = {
    "A": "77",
    "B": "88",
    "C": "99",
    "D": "88",
}

key_list = list(filter(lambda k: raw_dict.get(k) == "88", raw_dict.keys()))
print(key_list)  # ['B', 'D']


"""
def jzjc_report_number():
    last_jzjc_number = ReportLists.objects.filter(project_type='JZJC').count()
    if ReportLists.project_type == 'JZJC' and not last_jzjc_number:
        return 'DJJC0001'
    report_jzjc_no = last_jzjc_number.report_jzjc_no
    report_jzjc_int = int(report_jzjc_no.split('DJJC')[-1])
    width = 4
    new_report_jzjc_int = report_jzjc_int + 1
    formatted_jzjc = (width - len(str(new_report_jzjc_int))) * "0" + str(new_report_jzjc_int)
    new_report_jzjc_no = 'DJJC' + str(formatted_jzjc)
    return new_report_jzjc_no


def djjc_report_number():
    last_djjc_number = ReportLists.objects.filter(project_type='DJJC').count()
    if ReportLists.project_type == 'DJJC' and not last_djjc_number:
        return 'JZJC0001'
    report_djjc_no = last_djjc_number.report_djjc_no
    report_djjc_int = int(report_djjc_no.split('JZJC')[-1])
    width = 4
    new_report_djjc_int = report_djjc_int + 1
    formatted_djjc = (width - len(str(new_report_djjc_int))) * "0" + str(new_report_djjc_int)
    new_report_djjc_no = 'JZJC' + str(formatted_djjc)
    return new_report_djjc_no
"""


"""
def increment_report_number():
    last_report_number = ReportLists.objects.filter(project_type='JZJC').count()
    # last_djjc_number = ReportLists.objects.filter(project_type='DJJC').count()
    # last_report_number = ReportLists.objects.all().order_by('id').last()
    if not last_report_number:
        return 'MAG0001'
    # if not last_djjc_number:
        # return 'DJJC'
    report_no = last_report_number.report_no
    report_int = int(report_no.split('MAG')[-1])
    width = 4
    new_report_int = report_int + 1
    formatted = (width - len(str(new_report_int))) * "0" + str(new_report_int)
    new_report_no = 'MAG' + str(formatted)
    return new_report_no
"""


class TestLists(models.Model):
    """测试自动编号功能"""
    choice = (
        (0, '基桩检测'),
        (1, '地基基础'),
        (2, '隧道工程')
    )
    type_name = models.CharField(choices=choice, max_length=64, default='', verbose_name='类型')
