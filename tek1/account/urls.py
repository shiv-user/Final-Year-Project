from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib import admin
from .decorators import admin_required,recep_required
from django.contrib.auth.decorators import login_required

app_name = 'account'

urlpatterns = [
    path('about/',views.about,name='about'),
    path('support/',views.support,name='support'),
    path('home/',views.home,name='home'),
    path('password/', views.change_password, name='change_password'),
    path('accounts/signup/recep/', views.RecepSignUpView.as_view(), name='recep_signup'),
    path('accounts/signup/admin/', views.AdminSignUpView.as_view(), name='admin_signup'),
    path('user/', views.user_list),
    path('dashboard/',login_required(views.dashboard),name='dash'),
    path('search/', admin_required(views.HomePageView.as_view()),name='search'),
    path('search_result/', admin_required(views.SearchResultsView.as_view()),name='search_result'),
    path('display',views.display,name = 'display'),
    path('register',views.main),
    path('search_ans/', views.get_queryset2, name='search_results') ,
    path('vhome', login_required(views.HomePage2View.as_view()), name='vhome'),
    path('download/' , views.csv_view, name='download'),
    path('team/', views.team, name='team'),
    path('not_found',views.not_found, name='not_found'),
    
    # path('user/<int:pk>/', views.user_detail),
    # path('display',views.display),
]
