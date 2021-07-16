from django.db import models


class GroupName(models.Model):
    name = models.CharField(max_length=50)


class Position(models.Model):
    name = models.CharField(max_length=100)


class Employee(models.Model):
    first_name = models.CharField(max_length=100, default='empty')
    last_name = models.CharField(max_length=100, default='empty')
    description = models.TextField(default='empty')
    id_position = models.ForeignKey(Position, on_delete=models.CASCADE)


class EmployeesPhones(models.Model):
    sip_phone = models.IntegerField()
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="phones")


class Group(models.Model):
    id_group_name = models.ForeignKey(GroupName, on_delete=models.CASCADE)
    id_employees_phones = models.ForeignKey(EmployeesPhones, on_delete=models.CASCADE, related_name="group_name")


class Clients(models.Model):
    first_name = models.CharField(max_length=100, default='empty')
    last_name = models.CharField(max_length=100, default='empty')
    description = models.TextField(default='empty')


class ClientPhones(models.Model):
    phone_number = models.CharField(max_length=13)
    id_clients = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name="phones")


class Status(models.Model):
    name = models.CharField(max_length=100)


class Events(models.Model):
    id_asterisk = models.FloatField()
    id_client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    id_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    call_recording = models.CharField(max_length=500, default='empty')
