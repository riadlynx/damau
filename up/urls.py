from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^todod/(?P<todoid>[0-9]+)/',views.todod,name='todod'),
    url(r'^fich/(?P<fileid>[0-9]+)/',views.graph,name='graph'),
    url(r'^barrages/$',views.barrages,name='barrages'),
    url(r'^barrage/(?P<barrageid>[0-9]+)/',views.barrage,name='barrage'),
    url(r'^instrument/(?P<instrumentid>[0-9]+)/', views.fich, name='appareils'),
    url(r'^fichsup/(?P<fileid>[0-9]+)/',views.fichdelete,name='fichdelete'),
    url(r'^rapports/$', views.rapports, name='rapports'),
    url(r'^rapport/(?P<rapportid>[0-9]+)/', views.rapport, name='rapport'),

]