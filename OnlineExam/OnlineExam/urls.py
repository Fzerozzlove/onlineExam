"""OnlineExam URL Configuration

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
from django.urls import path
from django.conf.urls import url
from student import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^toIndex', views.index),
    url(r'^studentLogin/', views.studentLogin),
    url(r'^teacherLogin/', views.teacherLogin),
    url(r'^startExam/', views.startExam),
    url(r'^calGrade/', views.calGrade),
    url(r'^showGrade/', views.showGrade),
    url(r'^logout/', views.logout),
    url(r'^queryStudent/', views.queryStudent),
    url(r'^teacherRegister/', views.teacherRegister),
    url(r'^studentRegister/', views.studentRegister),
    url(r'^addq/', views.addq),
    url(r'^questionAddition/', views.questionAddition),
]
