from django.contrib import admin
from django.urls import path, re_path
from lists import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.home_page, name='home'),
]
