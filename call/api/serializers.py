from rest_framework import serializers
from .models import Events, ClientPhones, Clients, EmployeesPhones, Employee, Status, Position, GroupName, Group
from rest_framework.response import Response


# для сбора номеров из базы у определенной карточки
def get_phones(instance):
    try:
        phones = [i["phone_number"] for i in instance.phones.all().values()]
    except:
        phones = None
    return phones


class ClientsTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clients
        fields = ("id", "first_name", "last_name", "description")

    def to_representation(self, instance):
        inst = super().to_representation(instance)
        phones = get_phones(instance)
        if phones:
            inst["phones"] = phones
        return inst

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        phones = data.get("phones", None)
        if phones:
            ret["phones"] = set(phones)
        return ret

    def update(self, instance, validated_data):
        phones_model = set(i.phone_number for i in ClientPhones.objects.filter(id_clients=instance))
        phones = validated_data.pop("phones", None)
        if phones:
            for phone in phones_model.symmetric_difference(phones):
                if not ClientPhones.objects.filter(phone_number=phone, id_clients=instance).exists():
                    if not ClientPhones.objects.filter(phone_number=phone).exists():
                        ClientPhones.objects.create(phone_number=phone, id_clients=instance)
                else:
                    ClientPhones.objects.get(phone_number=phone).delete()
        inst = super().update(instance, validated_data)
        return inst


class ClientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clients
        fields = ("id", "first_name", "last_name", "description")

    def to_representation(self, instance):
        inst = super().to_representation(instance)
        phones = get_phones(instance)
        if phones:
            inst["phones"] = phones
        else:
            inst["phones"] = []
        return inst

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret["phones"] = []

        phones = data.get("phones", None)
        if phones:
            for phone in phones:
                if not ClientPhones.objects.filter(phone_number=phone).exists():
                    ret["phones"].append(phone)
        return ret

    def create(self, validated_data):
        phones = validated_data.pop("phones", None)
        client_card = Clients.objects.create(**validated_data)
        if phones:
            for phone in set(phones):
                ClientPhones.objects.create(id_clients=client_card, phone_number=phone)
        return validated_data


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("first_name", "last_name", "description", "id_position")

    def to_representation(self, instance):
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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["id_status"] = Status.objects.get(id=ret["id_status"]).name
        return ret

    def to_internal_value(self, data):
        number_client = data.pop("number_client", None)
        number_employee = data.pop("number_employee", None)
        ret = super().to_internal_value(data)
        if number_client:
            if ClientPhones.objects.filter(phone_number=number_client).exists():
                client_phones = ClientPhones.objects.get(phone_number=number_client)

            else:
                id_clients = Clients.objects.create()
                client_phones = ClientPhones.objects.create(phone_number=number_client, id_clients=id_clients)
            ret['id_client'] = client_phones.id_clients
        if number_employee:
            if EmployeesPhones.objects.filter(sip_phone=number_employee).exists():
                employee_phone = EmployeesPhones.objects.get(sip_phone=number_employee)
            else:
                position = Position.objects.get_or_create(name='None')
                employee = Employee.objects.create(id_position=position[0])
                employee_phone = EmployeesPhones.objects.create(sip_phone=number_employee, id_employee=employee)
                group_name = GroupName.objects.get_or_create(name='ALL')
                Group.objects.create(id_group_name=group_name[0], id_employees_phones=employee_phone)
            ret['id_employee'] = employee_phone.id_employee
        return ret

    def create(self, validated_data):
        Events.objects.create(**validated_data)
        return validated_data
