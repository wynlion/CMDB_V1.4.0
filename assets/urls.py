from django.urls import path
from assets import views

app_name = 'assets'


urlpatterns = [
    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('index/', views.index, name='index'),
    path('detail/<int:asset_id>/', views.detail, name='detail'),
    # path('allprojects/', views.allprojects, name='allprojects'),
    path('', views.dashboard),
    path('attachements/', views.attachements, name='attachments')
    # path('', views.attachements, name='attachments'),
]
