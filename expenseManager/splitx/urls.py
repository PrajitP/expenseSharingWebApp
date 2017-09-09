from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^login/$', login, {"template_name": 'splitx/login.html' }),
]
