from django.urls import include
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import url

router = DefaultRouter()

router.register(r'players', views.playerViewSet)
router.register(r'matchs', views.matchViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url('get_test',views.TestView.get_test),
    url('requestPlayer',views.requestPlayerView.request_player),
    url('getPlayer',views.requestPlayerView.get_player),
    url('getRune',views.runeView.get_rune),
    url('getItem',views.itemView.get_item),
    url('getMatch',views.matchView.get_match),
    url('getTimeLine',views.matchTimeLinePlayerView.get_time_line)
]