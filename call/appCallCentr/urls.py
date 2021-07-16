from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact_book', views.contact_book, name='contact_book'),
    path('contacts_book', views.contacts_book, name='contacts_book'),
    path('editing_contact/<pk>', views.editing_contact, name='load_layout'),
    path('del_num/<pk>', views.del_number, name='del_num'),
]
