from rest_framework import generics, permissions, status
from rest_framework.response import Response
from . import serializers
from rest_framework import mixins
from django.core.serializers import serialize
from .models import Events, Clients, ClientPhones, EmployeesPhones
from django.forms.models import model_to_dict


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
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class ClientCard(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Clients.objects.all()
#     serializer_class = serializers.ClientsSerializer

class ClientCardCreateGet(generics.ListCreateAPIView):
    queryset = Clients.objects.all()
    serializer_class = serializers.ClientsSerializer


class ClientCardEditingDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clients.objects.all()
    serializer_class = serializers.ClientsTestSerializer

