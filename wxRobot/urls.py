"""wxRobot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from login import views as login_views
from background import views as frame_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_views.main_index),
    path('index/',login_views.index),
    path('is_login/',login_views.is_login),
    path('logout/',frame_views.logout),
    path('Heart_rate_response/',frame_views.Heart_rate_response),

    path('home/',frame_views.home),
    path('data_analysis/',frame_views.data_analysis),
    path('custom_plug/',frame_views.custom_plug),
    path('timed_transmission/',frame_views.timed_transmission),
    path('intelligent_chat/',frame_views.intelligent_chat),


    # path('data_analysis',)



#     Dashboard  -> 数据分析  -> data_analysis
# Components -> 自定义插件管理  ->  custom_plug-in
# Notifications -> 定时发送  -> timed_transmission
# Typography ->  智能聊天 -> Intelligent_chat


]
