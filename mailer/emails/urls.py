from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^new_email/$', views.new_email, name="new_email"),
    url(r'^finish_email/$', views.finish_email, name="finish_email"),
]
