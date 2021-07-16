from rest_framework import generics, permissions, status
from rest_framework.response import Response
from . import serializers
from rest_framework import mixins
from django.core.serializers import serialize
from .models import Events, Clients, ClientPhones, EmployeesPhones
from django.forms.models import model_to_dict

# class ClientsDetails(generics.ListCreateAPIView):
#     queryset = ClientNumber.objects.all()
#     serializer_class = serializers.PhonesSerializer
#
#     def put(self, request, *args, **kwargs):
#         try:
#             puk = ClientNumber.objects.get(phone_number=request.data['phone_number'])
#             print('PUK ClientsDetails')
#         except:
#             return Response('Все в говне')
#         return Response(status=status.HTTP_200_OK)
#
#     def post(self, request, *args, **kwargs):
#         if ClientNumber.objects.filter(phone_number=request.data['phone_number']).exists():
#             return Response('Все в говне')
#         else:
#             # super(ClientsDetails, self).post(self, request, *args, **kwargs)
#             return self.create(request, *args, **kwargs)
#
#
# class EventsDetails(generics.ListCreateAPIView):
#     queryset = CallEvents.objects.all()
#     serializer_class = serializers.EventsSerializer
#
#     def put(self, request, *args, **kwargs):
#         try:
#             puk = CallEvents.objects.get(aster_id=request.data['aster_id'])
#             puk.event_id = States.objects.get(id=request.data['event_id'])
#             print(puk.event_id.state)
#             if request.data['number_sip'] != '':
#                 puk.number_sip = request.data['number_sip']
#             puk.save()
#         except Exception as exc:
#             return Response('Все в говне тут')
#
#         return Response(status=status.HTTP_200_OK)


class EventsViews(mixins.UpdateModelMixin, generics.ListCreateAPIView):
    queryset = Events.objects.all()
    serializer_class = serializers.EventsSerializer

    def put(self, request, *args, **kwargs):
        if request.data.get("id_asterisk") and Events.objects.filter(id_asterisk=request.data['id_asterisk']).exists():
            instance = Events.objects.get(id_asterisk=request.data['id_asterisk'])
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        else:

            return Response('ВСЕ В ГОВНЕ')


    # def post(self, request, *args, **kwargs):
    #     # request.data['id_client'] = model_to_dict(get_or_create_client(request.data['number_client']))
    #     # request.data['id_employee'] = get_or_create_employee(request.data['number_employee'])
    #     # print(request.data)
    #     # return Response(status=status.HTTP_200_OK)
    #     return self.create(request, *args, **kwargs)


'''
    "id_asterisk": 789.798,
    "number_client": 79172535561,
    "call_recording": "asd",
    "number_employee": 6666,
    "id_status": 1
'''