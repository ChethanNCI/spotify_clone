from django.urls import path
from . import views

urlpatterns = [
    path ('', views.index, name='index'),
    path ('login', views.login, name='login'),
    path ('signup', views.signup, name='signup'),
    path ('logout', views.logout, name='logout'),
    path('music/<str:pk>/', views.music, name='music'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('subscribe/', views.subscription_page, name='subscription_page'),
    path('process_subscription/', views.process_subscription, name='process_subscription'),
    path('process_unsubscription/', views.process_unsubscription, name='process_unsubscription'),
]
