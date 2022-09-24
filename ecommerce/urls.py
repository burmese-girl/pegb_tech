
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    ]