from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^test2/', views.test2, name='test2'),
	url(r'^test/', views.test, name='test'),
	url(r'^$',views.index,name = 'index'),
]
