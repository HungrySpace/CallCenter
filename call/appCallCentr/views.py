from django.shortcuts import render
from .forms import AddContactForm
# from .models import Client, ClientNumber
# from api.models import Events, States
from django.http import HttpResponseRedirect


def index(request):
    data = {'puk': 123}
    # data = Events.objects.all().values()
    #
    # for levent in data:
    #     levent["state"] = States.objects.get(id=levent["event_id_id"]).state
    #     if ClientNumber.objects.filter(phone_number=int(levent["number"])).exists():
    #         levent["card"] = ClientNumber.objects.get(phone_number=int(levent["number"])).client_id
    #     else:
    #         levent["card"] = levent["number"]
    return render(request, 'appCallCentr/index.html', {"data": data})


def editing_contact(request, pk):
    pass
    # if request.method == 'POST':
    #     form = AddContactForm(request.POST or None)
    #     if form.is_valid():
    #         card = Client.objects.get(id=pk)
    #         card.first_name = form.cleaned_data['first_name']
    #         card.last_name = form.cleaned_data['last_name']
    #         card.email = form.cleaned_data['email']
    #         card.description = form.cleaned_data['description']
    #         card.save()
    #
    #         print(ClientNumber.objects.filter(client_id=pk))
    #
    #         for i in request.POST.items():
    #             if str(i).find("number") > 0 and not ClientNumber.objects.filter(phone_number=i[1]):
    #                 num = ClientNumber(client_id=card, phone_number=i[1])
    #                 num.save()
    #     return HttpResponseRedirect('/contact_book')
    # else:
    #     card_client = Client.objects.filter(id=pk).values()[0]
    #     numbers = ClientNumber.objects.filter(client_id=pk).values()
    #     return render(request, 'appCallCentr/editing.html', {'card_client': card_client, "numbers": enumerate(numbers),
    #                                                          'count_num': len(numbers)})


def del_number(request, pk):
    pass
    # numbers = ClientNumber.objects.get(phone_number=pk)
    # id_client = str(numbers.client_id.id)
    # numbers.delete()
    # return HttpResponseRedirect('/editing_contact/' + id_client)


def contact_book(request):
    pass
    # form = AddContactForm(request.POST or None)
    # print(request.method, form.is_valid())
    # if request.method == 'POST' and form.is_valid():
    #     if not ClientNumber.objects.filter(phone_number=form.cleaned_data['number_0']):
    #         card = Client(first_name=form.cleaned_data['first_name'],
    #                       last_name=form.cleaned_data['last_name'],
    #                       email=form.cleaned_data['email'],
    #                       description=form.cleaned_data['description'])
    #         card.save()
    #         num = ClientNumber(client_id=card,
    #                            phone_number=form.cleaned_data['number_0'])
    #         num.save()
    #     else:
    #         print('LOOOOOOOOOOOOOOOOOOOOOOX')
    # dict_contact = {}
    # for obj_field in Client.objects.all():
    #     dict_contact[obj_field] = list(ClientNumber.objects.filter(client_id=obj_field.id))
    # return render(request, 'appCallCentr/contact_book.html', {"dict_contact": dict_contact})


def contacts_book(request):
    pass
    # dict_contact = {}
    # for obj_field in Client.objects.all():
    #     dict_contact[obj_field] = list(ClientNumber.objects.filter(client_id=obj_field.id))
    # return render(request, 'appCallCentr/contact_book.html', {"dict_contact": dict_contact})
