from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^quotes$', views.quotes),
    url(r'^display$', views.display),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    # url(r'^travels$', views.travel_dash),
    # url(r'^travels/add$', views.travel_form),
    url(r'^send_quote$', views.add_quote),
    url(r'^users/(?P<id>\d+)$', views.user_gen),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    # url(r'^travels/destination$', views.destination),
    url(r'^quotes/(?P<id>\d+)$', views.add_fav),

    ]