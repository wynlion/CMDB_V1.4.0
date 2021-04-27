"""CMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.urls import include
from django.views.static import serve
from CMDB import settings
from assets import views
from django.conf.urls.static import static
from assets.views import AttachmentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('assets/', include('assets.urls')),
    path('attachment/<int:pk>/', AttachmentView.as_view(), name='attachment'),
    path('projects/', include('projects.urls')),
    # path('media/', views.get_logfile),
    # path(r'media/file', views.get_logfile),
    # re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # path('show_upload', views.show_upload),
    # path('upload_handle', views.upload_handle),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
