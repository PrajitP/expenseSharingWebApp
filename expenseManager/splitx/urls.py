from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_reset, password_reset_done

from splitx import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^login/$', login, {"template_name": 'splitx/login.html' }),
    url(r'^logout/$', logout, {"template_name": 'splitx/logout.html' }),
    url(r'^register/$', views.register, name="register"),
    url(r'^profile/$', views.view_profile, name="view_profile"),
    url(r'^profile/edit/$', views.edit_profile, name="edit_profile"),
    url(r'^change_password$', views.change_password, name="change_password"),
    url(r'^expenses/add/$', views.add_expense, name="add_expense"),
]
