import random

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User as CustomUser

User = get_user_model()


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    template_name = 'main/index.html'


class RegisterView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        # current_site = Site.objects.get_current().domain

        send_mail(
            subject='Поздравляем с регистрацией!',
            message=f'Вы зарегистрировались на нашей платформе. Пожалуйста, перейдите по ссылке, чтобы подтвердить свой адрес электронной почты: http://127.0.0.1:8000/{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )
        return redirect('users:email_confirmation_sent')


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return  redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Письмо активации отправлено'
        return context_data


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Ваш электроный адрес активирован'
        return context_data


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Ваш электроный адрес не активирован'
        return context_data


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    success_url = reverse_lazy('users:profile')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    permission_required = ('users.view_all_users_user', 'users.block_user_user')


@login_required
def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('main:index'))


def toggle_activity(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active:
        user_item.is_active = False
    else:
        user_item.is_active = True

    user_item.save()
    return redirect(reverse('users:user_list'))
