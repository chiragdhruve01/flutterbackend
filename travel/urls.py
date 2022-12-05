from django.urls import path , re_path
from . import views
from django.contrib.auth import views as django_views

urlpatterns = [
    path('',views.index,name='index'),

    path('addCompany',views.addCompany.as_view(),name='addCompany'),
    path('addCompany',views.addCompany.as_view(),name='addCompany'),
    path('addState',views.addState.as_view(),name='addState'),
    path('signup',views.AdminRegister.as_view(),name='register'),
    path('companyList',views.companyList.as_view(),name="companyList"),
    path('companyDetail/<id>',views.companyDetails.as_view(),name="companyDetails"),
    path('stateList/<id>',views.comstateList.as_view(),name="stateList"),

]