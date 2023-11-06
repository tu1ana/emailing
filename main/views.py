from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django_apscheduler.jobstores import DjangoJobStore

from blog.models import Blog
from main.forms import EmailingForm, MessageForm, ClientForm
from main.models import Emailing, Log, Client, Message
from main.services import launch_scheduler
from users.models import User

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


class IndexView(TemplateView):
    """Количество рассылок, количество активных рассылок, количество уникальных клиентов для рассылок,
    3 случайные статьи из блога. Кеширование"""
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # random_pk = choice(Blog.objects.values_list('pk', flat=True))
        context_data = {
            'emailing_count': Message.objects.count(),
            'emailing_active_count': Message.objects.filter(is_active=True).count(),
            'client_count': User.objects.count(),
            # 'random_obj': Blog.objects.get(pk=random_pk)
            'random_blog_list': Blog.objects.order_by('?')[:3],
            'title': 'Сервис рассылок - Главная'
        }
        # pks = Blog.objects.values_list('pk', flat=True)
        # random_pk = choice(pks)
        # random_obj = Blog.objects.get(pk=random_pk)
        return context_data


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'Новой сообщение от {name} ({email}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'main/contact.html', context)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Рассылки'
        if self.request.user.has_perm('main.view_all_messages'):
            context_data['object_list'] = Message.objects.all()
        else:
            context_data['object_list'] = Message.objects.filter(auth_user=self.request.user)
        return context_data


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Emailing
    form_class = MessageForm
    success_url = reverse_lazy('main:list')
    extra_context = {'title': 'Создать рассылку'}

    def form_valid(self, form):
        self.object = form.save()
        self.object.auth_user = self.request.user
        self.object.save()

        log = Log.objects.create(server_response='-', status='создана', message=self.object)
        log.save()

        launch_scheduler(scheduler)

        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    extra_context = {'title': 'Просмотр рассылки'}


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:list')
    extra_context = {'title': 'Редактирование рассылки'}


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('main:list')
    extra_context = {'title': 'Удаление рассылки'}


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    extra_context = {'title': 'Логи рассылки'}
    # success_url = reverse_lazy('main:log_list')

    def get_queryset(self):
        queryset = super().get_queryset().filter(message_id=self.kwargs.get('pk'))
        queryset = queryset.order_by('-pk')

        return queryset


class EmailingCreateView(LoginRequiredMixin, CreateView):
    model = Emailing
    form_class = EmailingForm
    success_url = reverse_lazy('main:list')
    extra_context = {'title': 'Создание рассылки'}


# class EmailingUpdateView(UpdateView):
#     model = Emailing
#     form_class = EmailingForm
#     success_url = reverse_lazy('main:list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Клиенты'

        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')
    extra_context = {'title': 'Создание клиента'}


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    # success_url = reverse_lazy('main:client_update')
    extra_context = {'title': 'Редактирование клиента'}


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')
    extra_context = {'title': 'Удаление клиента'}


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    extra_context = {'title': 'Редактирование клиента'}


def toggle_activity_message(request, pk):
    item = get_object_or_404(Message, pk=pk)
    if item.is_active:
        item.is_active = False
    else:
        item.is_active = True

    item.save()
    return redirect(reverse('main:list'))
