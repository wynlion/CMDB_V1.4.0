from django.contrib import admin
from members import models
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


class StaffsAdmin(admin.ModelAdmin):
    list_per_page = 10


admin.site.register(models.Staffs, StaffsAdmin)
