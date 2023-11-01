from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django_apscheduler.jobstores import DjangoJobStore

from blog.models import Blog
from main.forms import EmailingForm, MessageForm, ClientForm
from main.models import Emailing, Log, Client, Message
from main.services import launch_scheduler

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


class IndexView(TemplateView):
    # количество рассылок, количество активных рассылок, количество уникальных клиентов для рассылок,
    # 3 случайные статьи из блога. Кеширование
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # context_data['object_list'] = Blog.objects.order_by('?')[:3]
        # random_pk = choice(Blog.objects.values_list('pk', flat=True))
        context_data = {
            'emailing_count': Message.objects.count(),
            'emailing_active_count': Message.objects.filter(is_active=True).count(),
            'client_count': Client.objects.count(),
            # 'random_obj': Blog.objects.get(pk=random_pk)
            'random_blog_list': Blog.objects.order_by('?')[:3],
            'title': 'Сервис рассылок - Главная'
        }
        # context_data['emailing_count'] = Emailing.objects.count()
        # context_data['emailing_active_count'] = Emailing.objects.filter(is_active=True).count()
        # context_data['client_count'] = Client.objects.count()
        # pks = Blog.objects.values_list('pk', flat=True)
        # random_pk = choice(pks)
        # random_obj = Blog.objects.get(pk=random_pk)
        return context_data


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'main/contact.html', context)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Рассылки'
        if self.request.user:
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
    success_url = reverse_lazy('main:log_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data().filter(message_id=self.kwargs.get('pk'))
        context_data = Log.objects.order_by('-pk')
        context_data['title'] = 'Логи рассылок'
        return context_data


class EmailingCreateView(LoginRequiredMixin, CreateView):
    model = Emailing
    form_class = EmailingForm
    success_url = reverse_lazy('main:list')
    extra_context = {'title': 'Создание рассылки'}

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     MessageFormset = inlineformset_factory(Emailing, Message, form=MessageForm, extra=1)
    #     if self.request.method == 'POST':
    #         context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
    #     else:
    #         context_data['formset'] = MessageFormset(instance=self.object)
    #     return context_data
    #
    # def form_valid(self, form):
    #     formset = self.get_context_data()['formset']
    #     self.object = form.save()
    #     if formset.is_valid():
    #         formset.instance = self.object
    #         formset.save()
    #
    #     return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    success_url = reverse_lazy('main:client_list')
    extra_context = {'title': 'Клиенты'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if Message.auth_user == self.request.user:
            context_data['object_list'] = Client.objects.filter()

        return context_data
    # def get_queryset(self):
    #     return super().get_queryset()


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_create')
    extra_context = {'title': 'Создание клиента'}

    # def form_valid(self, form):
    #     self.object = form.save()
    #     self.object.auth_user = self.request.user
    #     self.object.save()
    #
    #     return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    # success_url = reverse_lazy('main:client_update')
    extra_context = {'title': 'Редактирование клиента'}


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    extra_context = {'title': 'Удаление клиента'}


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    success_url = reverse_lazy('main:client_view')
    extra_context = {'title': 'Редактирование клиента'}

