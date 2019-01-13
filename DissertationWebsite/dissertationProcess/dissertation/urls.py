from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.StartView.as_view(), name='start' ),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('index/', views.index , name='index'),
    path('index/<username>/', views.UserIndexView.as_view(), name='userindex'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='dissertation/password_change_form.html'),name='password_change'),
    path('password-changed/', auth_views.PasswordChangeDoneView.as_view(template_name='dissertation/password_change_done.html'),name='password_change_done'),
]