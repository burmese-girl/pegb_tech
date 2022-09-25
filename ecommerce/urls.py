
from django.urls import path
from . import views
from . import api

app_name = 'user'

urlpatterns = [
    # path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('api/user_login/', api.LoginView.as_view()),
    path('api/add_product/', api.AddProductView.as_view()),
    ]