from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from multiselectfield import MultiSelectField
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
# Create your models here.


class Asset(models.Model):
    """所有资产的共有数据表"""

    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('software', '软件资产'),
    )

    asset_status = (
        (0, '入库'),
        (1, '出库'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )

    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name='资产类型')
    name = models.CharField(max_length=64, unique=True, verbose_name='资产名称')  # 不可重复
    sn = models.CharField(max_length=128, unique=True, verbose_name='资产序列号')
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name='所属业务线',
                                      on_delete=models.SET_NULL)

    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='设备状态')

    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name='制造商',
                                     on_delete=models.SET_NULL)
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='资产管理员', related_name='admin',
                              on_delete=models.SET_NULL)
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='所在机房', on_delete=models.SET_NULL)
    contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='合同', on_delete=models.SET_NULL)

    purchase_day = models.DateField(null=True, blank=True, verbose_name="购买日期")
    expire_day = models.DateField(null=True, blank=True, verbose_name="过保日期")
    price = models.FloatField(null=True, blank=True, verbose_name="价格")

    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name='批准人', related_name='approved_by',
                                    on_delete=models.SET_NULL)

    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    def __str__(self):
        return '<%s>  %s' % (self.get_asset_type_display(), self.name)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"
        ordering = ['-c_time']


class Server(models.Model):
    """服务器设备"""

    sub_asset_type_choice = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机'),
    )

    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 非常关键的一对一关联！asset被删除的时候一并删除server
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="服务器类型")
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name="添加方式")
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server',
                                  blank=True, null=True, verbose_name="宿主机", on_delete=models.CASCADE)  # 虚拟机专用字段
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='Raid类型')

    os_type = models.CharField('操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField('发行商', max_length=64, blank=True, null=True)
    os_release = models.CharField('操作系统版本', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"


class SecurityDevice(models.Model):
    """安全设备"""

    sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (4, '运维审计系统'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="安全设备类型")
    model = models.CharField(max_length=128, default='未知型号', verbose_name='安全设备型号')

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + str(self.model) + " id:%s" % self.id

    class Meta:
        verbose_name = '安全设备'
        verbose_name_plural = "安全设备"


class StorageDevice(models.Model):
    """存储设备"""

    sub_asset_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储器'),
        (2, '磁带库'),
        (4, '磁带机'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="存储设备类型")
    model = models.CharField(max_length=128, default='未知型号', verbose_name='存储设备型号')

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + str(self.model) + " id:%s" % self.id

    class Meta:
        verbose_name = '存储设备'
        verbose_name_plural = "存储设备"


class NetworkDevice(models.Model):
    """网络设备"""

    sub_asset_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (4, 'VPN设备'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="网络设备类型")

    vlan_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="VLanIP")
    intranet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="内网IP")

    model = models.CharField(max_length=128, default='未知型号',  verbose_name="网络设备型号")
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name="设备固件版本")
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name="端口个数")
    device_detail = models.TextField(null=True, blank=True, verbose_name="详细配置")

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"


class Software(models.Model):
    """
    只保存付费购买的软件
    """
    sub_asset_type_choice = (
        (0, '操作系统'),
        (1, '办公/开发软件'),
        (2, '业务软件'),
    )

    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="软件类型")
    license_num = models.IntegerField(default=1, verbose_name="授权数量")
    version = models.CharField(max_length=64, unique=True, help_text='例如: RedHat release 7 (Final)',
                               verbose_name='软件/系统版本')

    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = "软件/系统"


class IDC(models.Model):
    """实验室"""
    apparatus_status_type = (
        (0, '入库'),
        (1, '出库'),
        (2, '待检'),
        (4, '送检'),
        (5, '已标定'),
        (6, '未知'),
        (7, '故障'),
    )
    name = models.CharField(max_length=64, unique=True, default='', verbose_name="实验室名称")
    item = models.CharField(max_length=128, unique=False, default='', verbose_name='设备名称')
    apparatus_status = models.SmallIntegerField(choices=apparatus_status_type,default=0, verbose_name='设备状态')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')
    apparatus_available = models.BooleanField('是否可用', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '实验室'
        verbose_name_plural = "实验室"


class Manufacturer(models.Model):
    """厂商"""

    name = models.CharField('厂商名称', max_length=64, unique=True)
    telephone = models.CharField('支持电话', max_length=30, blank=True, null=True)
    memo = models.CharField('备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"


class BusinessUnit(models.Model):
    """业务线"""

    parent_unit = models.ForeignKey('self', blank=True, null=True, related_name='parent_level',
                                    on_delete=models.SET_NULL)
    name = models.CharField('业务线', max_length=64, unique=True)
    memo = models.CharField('备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"


class Contract(models.Model):
    """合同"""

    sn = models.CharField('合同号', max_length=128, unique=True)
    name = models.CharField('合同名称', max_length=64)
    memo = models.TextField('备注', blank=True, null=True)
    price = models.IntegerField('合同金额')
    detail = models.TextField('合同详细', blank=True, null=True)
    start_day = models.DateField('开始日期', blank=True, null=True)
    end_day = models.DateField('失效日期', blank=True, null=True)
    license_num = models.IntegerField('license数量', blank=True, null=True)
    c_day = models.DateField('创建日期', auto_now_add=True)
    m_day = models.DateField('修改日期', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"


class Tag(models.Model):
    """标签"""
    name = models.CharField('标签名', max_length=32, unique=True)
    c_day = models.DateField('创建日期', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = "标签"


class CPU(models.Model):
    """CPU组件"""

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 设备上的cpu肯定都是一样的，所以不需要建立多个cpu数据，一条就可以，因此使用一对一。
    cpu_model = models.CharField('CPU型号', max_length=128, blank=True, null=True)
    cpu_count = models.PositiveSmallIntegerField('物理CPU个数', default=1)
    cpu_core_count = models.PositiveSmallIntegerField('CPU核数', default=1)

    def __str__(self):
        return self.asset.name + ":   " + self.cpu_model

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = "CPU"


class RAM(models.Model):
    """内存组件"""

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField('SN号', max_length=128, blank=True, null=True)
    model = models.CharField('内存型号', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('内存制造商', max_length=128, blank=True, null=True)
    slot = models.CharField('插槽', max_length=64)
    capacity = models.IntegerField('内存大小(GB)', blank=True, null=True)

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = "内存"
        unique_together = ('asset', 'slot')  # 同一资产下的内存，根据插槽的不同，必须唯一


class Disk(models.Model):
    """硬盘设备"""

    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('unknown', 'unknown'),
    )

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField('硬盘SN号', max_length=128)
    slot = models.CharField('所在插槽位', max_length=64, blank=True, null=True)
    model = models.CharField('磁盘型号', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('磁盘制造商', max_length=128, blank=True, null=True)
    capacity = models.FloatField('磁盘容量(GB)', blank=True, null=True)
    interface_type = models.CharField('接口类型', max_length=16, choices=disk_interface_type_choice, default='unknown')

    def __str__(self):
        return '%s:  %s:  %s:  %sGB' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"
        unique_together = ('asset', 'sn')


class NIC(models.Model):
    """网卡组件"""

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)  # 注意要用外键
    name = models.CharField('网卡名称', max_length=64, blank=True, null=True)
    model = models.CharField('网卡型号', max_length=128)
    mac = models.CharField('MAC地址', max_length=64)  # 虚拟机有可能会出现同样的mac地址
    ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)
    net_mask = models.CharField('掩码', max_length=64, blank=True, null=True)
    bonding = models.CharField('绑定地址', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s:  %s:  %s' % (self.asset.name, self.model, self.mac)

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = "网卡"
        unique_together = ('asset', 'model', 'mac')  # 资产、型号和mac必须联合唯一。防止虚拟机中的特殊情况发生错误。


class EventLog(models.Model):
    """
    日志.
    在关联对象被删除的时候，不能一并删除，需保留日志。
    因此，on_delete=models.SET_NULL
    """

    event_type_choice = (
        (0, '其它'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线/更新/变更'),
    )

    name = models.CharField('事件名称', max_length=128)
    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批成功时有这项数据
    new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True, on_delete=models.SET_NULL)
    event_type = models.SmallIntegerField('事件类型', choices=event_type_choice, default=4)
    component = models.CharField('事件子项', max_length=256, blank=True, null=True)
    detail = models.TextField('事件详情')
    date = models.DateTimeField('事件时间', auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='事件执行人', on_delete=models.SET_NULL)
    memo = models.TextField('备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"


class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""

    sn = models.CharField('资产SN号', max_length=128, unique=True)  # 此字段必填
    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('software', '软件资产'),
    )
    asset_type = models.CharField(choices=asset_type_choice, default='server', max_length=64, blank=True, null=True,
                                  verbose_name='资产类型')

    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='生产厂商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    cpu_count = models.PositiveSmallIntegerField('CPU物理数量', blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField('CPU核心数量', blank=True, null=True)
    os_distribution = models.CharField('发行商', max_length=64, blank=True, null=True)
    os_type = models.CharField('系统类型', max_length=64, blank=True, null=True)
    os_release = models.CharField('操作系统版本号', max_length=64, blank=True, null=True)

    data = models.TextField('资产数据')  # 此字段必填

    c_time = models.DateTimeField('汇报日期', auto_now_add=True)
    m_time = models.DateTimeField('数据更新日期', auto_now=True)
    approved = models.BooleanField('是否批准', default=False)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"
        ordering = ['-c_time']


"""  已添加至projects App
class AllProjects(models.Model):
    项目总览（已添加至projects App）

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
"""


"""  已添加至projects App
class Member(models.Model):
    成员所属

    section_type_choice = (
        ('detection', '检测部'),
        ('integration', '综合部'),
        ('financial', '财务部'),
        ('security', '设备安全部'),
        ('management', '经营部'),
    )

    group_type_choice = (
        ('bridge-1', '桥梁1组'),
        ('bridge-2', '桥梁2组'),
        ('bridge-petrol', '桥梁巡检组'),
        ('road', '道路组'),
        ('tunnel', '隧道组'),
        ('material', '材料科研组'),
    )

    name = models.CharField('项目成员', max_length=64, unique=True)
    belong_to_section = models.CharField(choices=section_type_choice, max_length=64, default='', verbose_name='所属部门')
    belong_to_group = models.CharField(choices=group_type_choice, max_length=64, default='', verbose_name='所属小组')
    c_day = models.DateField('创建日期', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目成员'
        verbose_name_plural = "项目成员"
"""


def increment_report_number():
    last_report_number = ReportLists.objects.all().order_by('id').last()
    # last_djjc_number = ReportLists.objects.filter(project_type='DJJC').count()
    # last_report_number = ReportLists.objects.all().order_by('id').last()
    if not last_report_number:
        return 'MAG0001'
    report_number = last_report_number.report_number
    report_int = int(report_number.split('MAG')[-1])
    width = 4
    new_report_int = report_int + 1
    formatted = (width - len(str(new_report_int))) * "0" + str(new_report_int)
    new_report_no = 'MAG' + str(formatted)
    return new_report_no


def jzjc_report_number():
    last_report_number = ReportLists.objects.filter(project_type='JZJC').last()
    if not last_report_number:
        return 'JZJC0001'
    report_number = last_report_number.report_number
    report_int = int(report_number.split('JZJC')[-1])
    width = 4
    new_report_int = report_int + 1
    formatted = (width - len(str(new_report_int))) * "0" + str(new_report_int)
    new_report_no = 'JZJC' + str(formatted)
    return new_report_no


def djjc_report_number():
    # last_report_number = ReportLists.objects.all().order_by('id').last()
    last_report_number = ReportLists.objects.filter(project_type='DJJC').last()
    if not last_report_number:
        return 'DJJC0001'
    report_number = last_report_number.report_number
    report_int = int(report_number.split('DJJC')[-1])
    width = 4
    new_report_int = report_int + 1
    formatted = (width - len(str(new_report_int))) * "0" + str(new_report_int)
    new_report_no = 'DJJC' + str(formatted)
    return new_report_no


def report_no():
    report_type = ReportLists.project_type
    if report_type == '基桩检测':
        return jzjc_report_number()
    elif report_type == '地基基础':
        return djjc_report_number()


class ReportLists(models.Model):
    """报告总览"""

    project_type_choice = (
        ('JZJC', '基桩检测'),
        ('DJJC', '地基基础'),
        ('SDGC', '隧道工程'),
        ('GLYYJSZK', '公路营运技术状况'),
        ('HNTJGJC', '混凝土结构检测'),
        ('LJLMGC', '路基路面工程'),
        ('QLJG', '桥梁结构'),
        ('GCJCYCL', '工程监测与测量'),
        ('JTAQSS', '交通安全设施'),
        ('ZHXJC', '综合性检测'),
        ('ZXBG', '咨询报告'),
    )

    project_type = models.CharField(choices=project_type_choice, max_length=64, default='', verbose_name='报告类型')

    def save(self, *args, **kwargs):
        super(ReportLists, self).save(*args, **kwargs)
    # project_type_name = project_type
    project_name = models.CharField(max_length=64, unique=False, default='', verbose_name='项目名称')
    commissioned_units = models.CharField(max_length=64, unique=False, default='', verbose_name='委托单位')
    report_name = models.CharField(max_length=64, unique=False, default='', verbose_name='报告名称')
    report_date = models.DateField(null=True, blank=True, verbose_name='报告日期')
    report_number = models.CharField(max_length=500, unique=True, default='',
                                     blank=True, null=True, verbose_name='报告编号')
    seal_type = (
        ('detectSeal', '检测专用章'),
        ('CMASeal', 'CMA专用章'),
        ('officialSeal', '公章'),
    )

    seal = MultiSelectField(choices=seal_type, default='', verbose_name='盖章类型')
    report_type_choice = (
        ('report', '报告'),
        ('plan', '方案'),
        ('record', '纪录'),
        ('order', '委托单'),
        ('photo', '照片'),
    )
    report = MultiSelectField(choices=report_type_choice, default='', verbose_name='存档资料')
    memo = models.TextField('备注', null=True, blank=True)
    file = models.FileField(upload_to='static/file', null=True, verbose_name='上传文件')

    def __str__(self):
        return '%s: %s: %s: %s: %s' % (self.project_name, self.commissioned_units, self.report_name, self.report_date,
                                       self.report_number)

    class Meta:
        verbose_name = '报告总览'
        verbose_name_plural = '报告总览'


class LogFile(models.Model):
    """"上传文件"""
    file = models.FileField(u'文件', upload_to='media/file/', null=True, blank=True)
    headshot = models.ImageField(null=True, blank=True, upload_to='media/image/', verbose_name='图片上传')
    file_name = models.CharField(u'文件名称', max_length=128, default='logfile_name', null=False)
    create_time = models.DateTimeField(u'创建时间', null=False)
    host_ip = models.CharField(u'主机IP', max_length=128, default='10.168.1.113', null=False)
    memo = models.CharField(u'备注说明', max_length=128, default='', null=False)

    class Meta:
        verbose_name = '文件上传'
        verbose_name_plural = '文件上传'


class Attachment(models.Model):
    """规范总览（包含规范的上传和下载功能）"""

    standard_type_choice = (
        ('CHL', '掺合料'),
        ('DL', '道路'),
        ('DJJZ', '地基、基桩'),
        ('FMH', '粉煤灰'),
        ('GJ', '钢筋'),
        ('HX', '化学'),
        ('HNT', '混凝土'),
        ('JL', '集料'),
        ('JC', '监测'),
        ('JA', '交安'),
        ('JS', '金属'),
        ('KZF', '矿渣粉'),
        ('LQ', '沥青'),
        ('QT', '其他'),
        ('QH', '桥涵'),
        ('SN', '水泥'),
        ('SD', '隧道'),
        ('TG', '土工'),
    )

    box_type_choice = (
        ('1', '①'), ('2', '②'), ('3', '③'), ('4', '④'), ('5', '⑤'), ('6', '⑥'),
        ('7', '⑦'), ('8', '⑧'), ('9', '⑨'), ('10', '⑩'),
    )

    file_type_choice = (
        ('word文档_07', 'docx'),
        ('excel文档_07', 'xlsx'),
        ('图片_1', 'JPEG'),
        ('图片_2', 'PNG'),
    )

    update_type_choice = (
        ('status_1', '已更新'),
        ('status_2', '未更新'),
        ('status_1', '已作废'),
    )

    standard_type = models.CharField(choices=standard_type_choice, max_length=64, default='', verbose_name='类别')
    box_type = models.CharField(choices=box_type_choice, max_length=4, default='', verbose_name='所在盒子')
    number = models.CharField(max_length=4, default='', verbose_name='序号')
    name = models.CharField(max_length=128, verbose_name='规范标准名称')
    standard_ID = models.CharField(max_length=64, unique=True, default='', verbose_name='标准编号')
    in_standard_ID = models.CharField(max_length=64, unique=True, default='', verbose_name='公司内部编号')
    memo = models.TextField('备注', null=True, blank=True)
    update_type = models.CharField(choices=update_type_choice, max_length=8, default='', verbose_name='更新情况')
    file = models.FileField(upload_to='static/file', null=True, verbose_name='上传规范')
    file_type = models.CharField(choices=file_type_choice, max_length=64, default='', verbose_name='文件类型')
    # file_name = str(name) + '.' + str(file_type)

    class Meta:
        verbose_name = '规范总览'
        verbose_name_plural = '规范总览'


class DeviceList(models.Model):
    """仪器总表（包含出入库登记功能）"""

    device_type_choice = (
        ('GJLSB', '钢筋类设备'),
        ('HXLSB', '化学类设备'),
        ('JLLSB', '集料类设备'),
        ('JALSB', '交安类设备'),
        ('LQHHLSB', '沥青混合料设备'),
        ('LQLSB', '沥青类设备'),
        ('QLLSB', '桥梁类设备'),
        ('SNHNTLSB', '水泥混凝土类设备'),
        ('SNLSB', '水泥类设备'),
        ('SNWJJLSB', '水泥外加剂类设备'),
        ('TGLSB', '土工类设备'),
        ('WJJHLSB', '无机结合料设备'),
        ('XCJCLSB', '现场检测类设备'),
        ('YSLSB', '岩石类设备'),
        ('ZHLSB', '综合类设备'),
    )

    situation_type_choice = (
        ('LH', '良好'),
        ('TY', '停用'),
    )

    room_type_choice = (
        ('')
    )

    next_type_choice = (
        ('CK', '出库'),
        ('RK', '入库'),
        ('SJ', '送检'),
        ('DJ', '待检')
    )

    device_number = models.CharField(max_length=64, unique=True, default='', verbose_name='仪器设备编号')
    device_name = models.CharField(max_length=64, default='', verbose_name='仪器设备名称')
    device_type = models.CharField(choices=device_type_choice, max_length=64, default='', verbose_name='仪器设备类别')
    size = models.CharField(max_length=64, default='', verbose_name='型号规格')
    accuracy = models.CharField(max_length=64, default='', verbose_name='量程/准确的(精度)')
    out_sn = models.CharField(max_length=64, unique=True, default='', verbose_name='出厂编号')
    purchase_date = models.DateField(null=True, blank=True, verbose_name='购置日期')
    situation_type = models.CharField(choices=situation_type_choice, max_length=64, default='', verbose_name='仪器设备状态')
    next_type = models.CharField(choices=next_type_choice, max_length=64, default='', verbose_name='设备下一步状态')

    class Meta:
        verbose_name = '设备管理'
        verbose_name_plural = '设备管理'


"""新增测试功能"""


"""  上传功能
    def file_name_download(self):
        return mark_safe('<a href="/media/file/{0}" download>{1}</a>'.format(
            self.file_name, self.file_name))
            
    file_name_download.short_description = 'Download Filename'
"""

"""  LogFile中的功能  待开发
    def __str__(self):
        return self.file_name
        
    @staticmethod
    def headshot_image(self):
        if self.image:
            return format_html(
                '<img src="/media/{}" width="156px" height="98px"/>',
                self.image,
            )
        else:
            return format_html(
                '<img src="/media/无拍照上传.png" width="156px" height="98px"/>',
            )
            
    headshot_image.short_description = "现场照片"
"""


"""  待开发
class Article(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=10)
    text = models.CharField(max_length=200)
    # 图片上传
    img = models.ImageField(upload_to='media')
    # 文件上传
    file_upload = models.FileField(upload_to='media')


# 创建一个记录阅读数量的模型
class ReadNum(models.Model):
    read_num_data = models.IntegerField()
    article = models.OneToOneField('Article', on_delete=models.DO_NOTHING)
"""

