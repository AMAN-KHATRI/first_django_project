from django.conf.urls import url
from AppOne import views

app_name = 'AppOne'

urlpatterns = [ 
	url(r'userlogin/', views.user_login, name = 'user_login'), 
	url(r'^/$', views.index, name = 'index'),
	url(r'register/', views.register, name = 'register')
]