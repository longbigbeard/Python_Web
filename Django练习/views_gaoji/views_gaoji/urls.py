"""views_gaoji URL Configuration

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
from django.urls import path, include
from front import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.template_csv, name='index'),
    # path('', views.large_csv, name='index'),
    path('add_title/', views.add_article, name='add_title'),
    # path('add_title/', views.AddBookView.as_view(), name='add_title'),
    path('', views.BookListView.as_view(), name='booklist'),
    # 如果渲染的模板不需要传递任何参数，只需要在这里进行映射就好了
    # path('about/', TemplateView.as_view(template_name='about.html') )
    path('about/', views.AboutView.as_view()),

    path('article/', include('front.urls'))

]
