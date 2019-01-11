"""ghoasite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import index,level_one,level_two,home,chart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('home/',home,name='home'),
    path('user/',include('user.urls')),
    path('subject/',include('subject.urls')),
    path('level_one/<int:sbo_pk>',level_one,name='level_one'),
    path('level_two/<int:sbt_pk>',level_two,name='level_two'),
    path('chart',chart,name='chart'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)