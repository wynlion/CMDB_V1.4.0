from django.contrib import admin
from projects import models
from assets import asset_handler
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from assets.models import ReportLists
from openpyxl import Workbook
from django.http import HttpResponse
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from io import StringIO
from datetime import date
from CMDB import settings
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.admin import widgets

# Register your models here.


class TestAdmin(admin.ModelAdmin):
    list_display = ['test']


class AllProjectsAdmin(admin.ModelAdmin):
    list_display = ['project_type', 'project_name', 'charge_person', 'members', 'project_status',
                    'project_status_percent', 'former_status_percent', 'start_day', 'expect_finished_day', 'memo']

    def members(self, obj):
        return [bt.name for bt in obj.group_members.all()]
    members.short_description = '项目成员'
    filter_horizontal = ['group_members']
    list_filter = ['project_type', 'project_status']
    list_per_page = 10


admin.site.register(models.Test, TestAdmin)
admin.site.register(models.AllProjects, AllProjectsAdmin)
