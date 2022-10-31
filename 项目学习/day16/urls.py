"""day16 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from app01 import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    
    #http://127.0.0.1:8000/depart/4(一个整型数字)/edit/
    path('depart/<int:nid>/edit/', views.depart_edit),
    
    path('user/list/',views.user_list),
    path('user/add/', views.user_add),
    path('user/modelform/add/', views.user_modelform_add),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/<int:nid>/delete/', views.user_delete),
    path('mobile/list/',views.mobile_list),
    path('mobile/add/',views.mobile_add),
    path('mobile/<int:nid>/edit/', views.mobile_edit),
    path('mobile/<int:nid>/delete/', views.mobile_delete),
    path('admin/list/',views.admin_list),
    path('admin/add/',views.admin_add),
    path('admin/<int:nid>/edit/',views.admin_edit),
    path('admin/<int:nid>/delete/',views.admin_delete),
    path('admin/<int:nid>/reset/',views.admin_reset)
]
