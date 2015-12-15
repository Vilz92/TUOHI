from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ilmoittautuminen, name='ilmoittautuminen'),
    url(r'^$', views.rekisteriseloste, name='rekisteriseloste'),
]