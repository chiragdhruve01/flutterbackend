from django.urls import path , re_path
from . import views
from django.contrib.auth import views as django_views

urlpatterns = [
    path('',views.index,name='index'),

    path('signup',views.AdminRegister.as_view(),name='register'),
    path('userDetails',views.userDetails.as_view(),name="userDetails"),

]