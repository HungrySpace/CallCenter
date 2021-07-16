from rest_framework import serializers
from .models import Events, ClientPhones, Clients, EmployeesPhones, Employee, Status, Position, GroupName, Group


class ClientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clients
        fields = ("first_name", "last_name", "description")

    def to_representation(self, instance):
        # объекты в примитивы
        inst = super().to_representation(instance)
        inst["phones"] = [i["phone_number"] for i in instance.phones.all().values()]
        return inst

    def to_internal_value(self, data):
        instance = super().to_internal_value(data)
        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("first_name", "last_name", "description", "id_position")

    def to_representation(self, instance):
        # объекты в примитив
        inst = super().to_representation(instance)
        dict_phones = {}
        for em_phone in instance.phones.all():
            dict_phones[em_phone.sip_phone] = [i.id_group_name.name for i in em_phone.group_name.all()]
        inst["phones"] = dict_phones
        inst["id_position"] = instance.id_position.name
        return inst


class EventsSerializer(serializers.ModelSerializer):
    id_client = ClientsSerializer(required=False)
    id_employee = EmployeeSerializer(required=False)

    class Meta:
        model = Events
        fields = ("id", "id_asterisk", "id_client", "id_employee", "call_recording", "id_status")

    def create(self, validated_data):
        Events.objects.create(**validated_data)
        return validated_data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["id_status"] = Status.objects.get(id=ret["id_status"]).name
        return ret

    def to_internal_value(self, data):
        number_client = data.pop("number_client", None)
        number_employee = data.pop("number_employee", None)
        instance = super().to_internal_value(data)
        if number_client:
            if ClientPhones.objects.filter(phone_number=number_client).exists():
                client_phones = ClientPhones.objects.get(phone_number=number_client)

            else:
                id_clients = Clients.objects.create()
                client_phones = ClientPhones.objects.create(phone_number=number_client, id_clients=id_clients)
            instance['id_client'] = client_phones.id_clients
        if number_employee:
            if EmployeesPhones.objects.filter(sip_phone=number_employee).exists():
                employee_phone = EmployeesPhones.objects.get(sip_phone=number_employee)
            else:
                position = Position.objects.get_or_create(name='None')
                employee = Employee.objects.create(id_position=position[0])
                employee_phone = EmployeesPhones.objects.create(sip_phone=number_employee, id_employee=employee)
                group_name = GroupName.objects.get_or_create(name='ALL')
                group = Group.objects.create(id_group_name=group_name[0], id_employees_phones=employee_phone)
            instance['id_employee'] = employee_phone.id_employee
        return instance

# class ClientNumberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientNumber
#         fields = "__all__"


# class ClientsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = ['first_name', 'last_name', 'email', 'job_title', 'description']
#
#
# class PhonesSerializer(serializers.ModelSerializer):
#     client_id = ClientsSerializer(required=False)
#
#     class Meta:
#         model = ClientNumber
#         fields = ['phone_number', 'client_id']
#
#     def create(self, validated_data):
#         validated_data['client_id'] = Client.objects.create(**validated_data['client_id'])
#         ClientNumber.objects.create(**validated_data)
#         return validated_data
#
#
# class StatesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = States
#         fields = ['id', 'state']
#
#
# class EventsSerializer(serializers.ModelSerializer):
#     number = PhonesSerializer(required=False)
#     event_id = StatesSerializer(required=False)
#
#     class Meta:
#         model = CallEvents
#         fields = ['aster_id', 'number', 'number_sip', 'date', 'event_id', 'date_end']
#
#     # записываем новый ивент
#     def create(self, validated_data):
#         # проверяем есть ли такой номер телефона в звписной книге
#         print('**********************************************')
#         # print(validated_data)
#         print(validated_data)
#         print('**********************************************')
#         if ClientNumber.objects.filter(phone_number=int(validated_data['number']['phone_number'])).exists():
#             validated_data['number'] = ClientNumber.objects.get(phone_number=validated_data['number']['phone_number'])
#         else:
#             validated_data['number']['client_id'] = Client.objects.create(**validated_data['number']['client_id'])
#             validated_data['number'] = ClientNumber.objects.create(**validated_data['number'])
#
#         validated_data['event_id'] = States.objects.get(id=validated_data['event_id']['state'])
#         CallEvents.objects.create(**validated_data)
#         return validated_data
