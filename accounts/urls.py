from django.urls import path
from . import views
from .views import register, user_login, user_logout, CustomPasswordChangeView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('accounts/profile/edit/', views.edit_profile, name='edit_profile'),
    path('password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('accounts/password/', views.CustomPasswordChangeView.as_view(), name='change_password')
]

