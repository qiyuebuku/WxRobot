<<<<<<< HEAD
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
from initialize import views as initialize_views
from homepage import views as homepage_views
from logIntoRegister import views as login_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',initialize_views.main_index),
    path('login/',login_views.login),
    path('register/',login_views.register),
    path('wx_init/',initialize_views.wx_init),
    path('init/',initialize_views.init),
    # path('wx_status/',initialize_views.wx_status),
    # path('logout/',homepage_views.logout),
    # path('Heart_rate_response/',homepage_views.Heart_rate_response),
    # path('analysis_result/',homepage_views.analysis_result),    
    path('save_chat_config/',homepage_views.save_chat_config),
    path('mainpage/',homepage_views.mainpage),
    path('test/',homepage_views.test),
    path('set_plugin_state/',homepage_views.set_plugin_state),
    path('save_clues/',homepage_views.save_clues),
    path('save_timer_send/',homepage_views.save_timer_send),
    path('del_plug/',homepage_views.del_plug),
    path('add_user_plug/',homepage_views.add_user_plug),
    path('get_plug_shops/',homepage_views.get_plug_shops),
    path('logout/',homepage_views.logout),




    
    

    
    
    # path('intelligent_switch/',homepage_views.intelligent_switch),
]
=======
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
from initialize import views as initialize_views
from homepage import views as homepage_views
from logIntoRegister import views as login_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',initialize_views.main_index),
    path('login/',login_views.login),
    path('register/',login_views.register),
    path('wx_init/',initialize_views.wx_init),
    # path('wx_status/',initialize_views.wx_status),
    # path('logout/',homepage_views.logout),
    # path('Heart_rate_response/',homepage_views.Heart_rate_response),
    # path('analysis_result/',homepage_views.analysis_result),    
    path('save_chat_config/',homepage_views.save_chat_config),
    path('mainpage/',homepage_views.mainpage),
    path('test/',homepage_views.test),
    path('set_plugin_state/',homepage_views.set_plugin_state)
    # path('intelligent_switch/',homepage_views.intelligent_switch),
]
>>>>>>> acb8c86e5915306157008056c793ddc27ee3fd97
