
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('user_details/', views.user_details),
    path('user_referrals/', views.user_referrals),
]