from django.urls import path
from . import views


urlpatterns = [
    path("",views.home,name="home"),
    path("send/",views.send,name="send"),
    path("sending/",views.sending,name="sending"),
    path("sendingToMany/",views.sendingToMany,name="sendingToMany"),
    path("customToMany/",views.customOneToMany,name="customOneToMany"),
    path("mobile/",views.mobile,name="mobile"),

]