"""tushu03 URL Configuration

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
from AppLibrary import views

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('add_data/', views.add_data),  # 添加数据使用
    path(r'', views.index_book),
    path(r'index_book/', views.index_book),
    path(r'add_book/', views.AddBook.as_view()),
    path(r'edit_book/', views.EditBook.as_view()),
    path(r'del_book/', views.del_book),

    path(r'index_author/', views.index_author),
    path(r'add_author/', views.AddAuthor.as_view()),
    path(r'edit_author/', views.EditAuthor.as_view()),
    path(r'del_author/', views.del_author),

    path(r'index_publish/', views.index_publish),
    path(r'add_publish/', views.AddPub.as_view()),
    path(r'edit_publish/', views.EditPub.as_view()),
    path(r'del_publish/', views.del_publish),

    path(r'login/', views.Login.as_view()),
    path(r'register/', views.Register.as_view()),
    path(r'logout/', views.logout),
    path(r'valid_img/', views.valid_img),
    path(r'confirm/', views.confirm),
]
