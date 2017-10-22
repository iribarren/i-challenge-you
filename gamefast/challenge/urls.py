from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^games/$', views.game_index, name='game_index'),
    url(r'^(?P<challenge_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?games/P<challenge_id>[0-9]+)/$', views.game_detail, name='game_detail'),

]

