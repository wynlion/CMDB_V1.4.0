from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from assets import models
from assets import asset_handler
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect
from django.http import FileResponse
from django.utils.http import urlquote
from .models import LogFile
# from CMDB.settings import MEDIA_ROOT
from assets.models import Attachment
from CMDB import settings
from django.views.generic.detail import DetailView
from django.views.generic.base import ContextMixin


def index(request):
    """
    资产总表视图
    :param request:
    :return:
    """
    assets = models.Asset.objects.all()
    return render(request, 'assets/index.html', locals())


def dashboard(request):
    total = models.Asset.objects.count()
    upline = models.Asset.objects.filter(status=0).count()
    offline = models.Asset.objects.filter(status=1).count()
    unknown = models.Asset.objects.filter(status=2).count()
    breakdown = models.Asset.objects.filter(status=3).count()
    backup = models.Asset.objects.filter(status=4).count()

    up_rate = round(upline / total * 100)
    o_rate = round(offline / total * 100)
    un_rate = round(unknown / total * 100)
    bd_rate = round(breakdown / total * 100)
    bu_rate = round(backup / total * 100)

    server_number = models.Server.objects.count()
    networkdevice_number = models.NetworkDevice.objects.count()
    storagedevice_number = models.StorageDevice.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    software_number = models.Software.objects.count()

    return render(request, 'assets/dashboard.html', locals())


def detail(request, asset_id):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param asset_id:
    :return:
    """

    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'assets/detail.html', locals())


def allprojects(request):
    """
    项目总览示意图
    :param request:
    :return:
    """
    projects = models.AllProjects.objects.all()
    return render(request, 'assets/allprojects.html', locals())


@csrf_exempt
def report(request):
    if request.method == 'POST':
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        if not data:
            return HttpResponse('没有数据！')
        if not issubclass(dict, type(data)):
            return HttpResponse('数据必须为字典格式！')
        # 你的检测代码

        sn = data.get('sn', None)

        if sn:
            asset_obj = models.Asset.objects.filter(sn=sn)  # [obj]
            if asset_obj:
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse('资产数据已经更新。')
            else:
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse('没有资产sn，请检查数据内容！')

    return HttpResponse('200 ok')


class AttachmentView(DetailView):
    queryset = Attachment.objects.all()
    slug_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if settings.DEBUG:
            response = HttpResponse(instance.file, content_type='application/force-download')
        else:
            # x-sendfile is a module of apache,you can replace it with something else
            response = HttpResponse(content_type='application/force-download')
            response['X-Sendfile'] = instance.file.path
        response['Content-Disposition'] = 'attachment; filename={}'.format(urlquote(instance.name))
        return response


"""新增测试功能"""

"""  待开发
def get_logfile(request):
    file_name = request.path.split('/')[-1]
    return redirect('http://10.168.1.113:8000/media/file' + '/' + file_name)
"""


"""
def download_file(request):
    file_name = request.path.split('/')[-1]
    return HttpResponseRedirect('http://10.168.1.113:8000/static' + '/' + file_name)
"""


""""
# /show_upload

def show_upload(request):
    return render(request, 'assets/uploadfiles.html')

# /upload_handle
# 图上上传处理,图片2种类型：
# 小于2.5M放在内存中：<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
# 大于2.5放在硬盘上：<class 'django.core.files.uploadedfile.TemporaryUploadedFile'>


def upload_handle(request):
    # (1)得到图片
    pic = request.FILES['pic']
    # (2)拼接图片保存路径+图片名
    save_path = "%s/media/%s" % (MEDIA_ROOT, pic.name)
    # (3)保存图片到指定路径，因为图片是2进制式，因此用wb，
    with open(save_path, 'wb') as f:
        # pic.chunks()为图片的一系列数据，它是一段段的，所以要用for逐个读取
        for content in pic.chunks():
            f.write(content)

    # (4)保存图片路径到数据库，此处只保存其相对上传目录的路径
    LogFile.objects.create(goods_pic='media/%s' % pic.name)

    # (5)别忘记返回信息
    return HttpResponse('上传成功，图片地址：media/%s' % pic.name)
"""