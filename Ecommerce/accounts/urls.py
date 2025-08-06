from django.urls import path
from . import views


app_name = 'accounts'  # namespace

urlpatterns = [
    path('register', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.dashboard_view, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
]
