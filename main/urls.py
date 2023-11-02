from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import IndexView, contact, MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, \
    MessageDeleteView, ClientListView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView, ClientDetailView, LogListView, EmailingCreateView

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(60)(IndexView.as_view()), name='index'),
    path('contact/', contact, name='contact'),
    path('list/', MessageListView.as_view(), name='list'),
    path('create/', MessageCreateView.as_view(), name='create'),
    path('view/<int:pk>', MessageDetailView.as_view(), name='view'),
    path('update/<int:pk>', MessageUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', MessageDeleteView.as_view(), name='delete'),
    path('logs/<int:pk>', LogListView.as_view(), name='log_list'),
    path('emailing/create/', EmailingCreateView.as_view(), name='emailing_create'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('client/view/<int:pk>', ClientDetailView.as_view(), name='client_view'),
]
