from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^register/$', views.sign_up, name="register"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout_user, name="logout"),
]
