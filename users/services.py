from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class UserNotAuthenticated(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Пользователь с таким email существует.')
            raise PermissionDenied
        return True

    def handle_no_permission(self):
        return redirect('main:index')
