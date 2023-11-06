from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, generate_new_password, UserUpdateView, toggle_activity, \
    UserListView, EmailConfirmationSentView, UserConfirmEmailView, EmailConfirmedView, EmailConfirmationFailedView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('profile/generate_password/', generate_new_password, name='generate_new_password'),
    path('activity/<int:pk>', toggle_activity, name='toggle_activity'),

    path('confirm_email/<str:uidb64>/<str:token>', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmation_sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('email_confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('email_confirmation_failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

]
