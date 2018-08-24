from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^score/$', views.score_list, name='score_list'),
    url(r'^daily/(?P<date>.+)/$', views.daily_score),
    url(r'^monthly/(?P<date>.+)/$', views.monthly_score),
    url(r'^score/new/$',views.post)
]