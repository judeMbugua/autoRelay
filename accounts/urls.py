from django.urls import path
from . import views
from main.views import home 

urlpatterns = [
	path("register/",views.register,name="register"),
  	path("login/",views.signIn,name="login"),
   	path("logout/",views.log_out,name="logout"),
    path("home/",home,name="home"),

]