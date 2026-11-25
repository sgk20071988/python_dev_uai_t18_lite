from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('register/success/', views.register_success_view, name='register_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('message/', views.message_view, name='message'),
    path('message/ajax/', views.message_ajax_view, name='message_ajax'),
    path('profile/', views.profile_view, name='profile'),
]