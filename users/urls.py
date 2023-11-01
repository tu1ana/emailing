from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, generate_new_password, UserUpdateView

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/generate_password/', generate_new_password, name='generate_new_password')
]
