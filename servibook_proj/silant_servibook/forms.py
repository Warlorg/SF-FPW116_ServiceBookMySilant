from django import forms
from django.contrib.flatpages.models import FlatPage
from django.core.exceptions import ValidationError

from .models import Vehicle, Maintenance, Reclamation, Client, ServiceDepartment


class VehicleForm(forms.ModelForm):
    shipment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Дата отгрузки с завода")

    class Meta:
        model = Vehicle
        fields = [
            "vehicle_model",
            "vehicle_number",
            "engine_model",
            "engine_number",
            "transmission_model",
            "transmission_number",
            "drive_axle_model",
            "drive_axle_number",
            "steer_axle_model",
            "steer_axle_number",
            "delivery_contract",
            "shipment_date",
            "end_user",
            "shipping_address",
            "configuration",
            "service_department",
            "customer",
        ]

        labels = {
            "vehicle_model": "Модель техники",
            "vehicle_number": "Заводской № машины",
            "engine_model": "Модель двигателя",
            "engine_number": "Заводской № двигателя",
            "transmission_model": "Модель трансмиссии",
            "transmission_number": "Заводской № трансмиссии",
            "drive_axle_model": "Модель ведущего моста",
            "drive_axle_number": "Заводской № ведущего моста",
            "steer_axle_model": "Модель управляемого моста",
            "steer_axle_number": "Заводской № управляемого моста",
            "delivery_contract": "Договор поставки (№, дата)",
            "shipping_address": "Адрес поставки (эксплуатации)",
            "shipment_date": "Дата отгрузки с завода",
            "end_user": "Грузополучатель (конечный потребитель)",
            "configuration": "Комплектация (доп. опции)",
            "service_department": "Сервисная компания",
            "customer": "Покупатель"
        }

        widgets = {
            'configuration': forms.Textarea(attrs={"rows": "3", "cols": "23"}),
        }


class MaintenanceForm(forms.ModelForm):
    maintenance_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                       input_formats=['%Y-%m-%d'], label="Дата проведения ТО")
    order_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),
                                 input_formats=['%Y-%m-%d'], label="Дата заказ-наряда")

    class Meta:
        model = Maintenance
        fields = [
            "vehicle",
            "type",
            "maintenance_date",
            "operating_time",
            "order_date",
            "order_number",
            "maintenance_service",
        ]

        labels = {
            "vehicle": "Машина",
            "type": "Вид ТО",
            "maintenance_date": "Дата проведения ТО",
            "operating_time": "Наработка, м/час",
            "order_date": "Дата заказ-наряда",
            "order_number": "Номер заказ-наряда",
            "maintenance_service": "Организация, проводившая ТО",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs["initial"]["user"]
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user in users_customers:
            self.fields["vehicle"] = forms.ModelChoiceField(queryset=Vehicle.objects.filter(customer__user=user))
        elif user in users_service_deps:
            self.fields["vehicle"] = forms.ModelChoiceField(
                queryset=Vehicle.objects.filter(service_department__user=user)
            )
        self.fields["vehicle"].label = "Машина"

    def clean(self):
        cleaned_data = super().clean()
        operating_time = cleaned_data.get("operating_time")
        if operating_time < 0:
            raise ValidationError({"operating_time": "Время наработки не может быть отрицательным!"})
        maintenance_date = cleaned_data.get("maintenance_date")
        order_date = cleaned_data.get("order_date")
        if maintenance_date and order_date > maintenance_date:
            raise ValidationError({"order_date": "Дата заказ-наряда не может быть больше Даты проведения ТО!"})
        return cleaned_data


class ReclamationForm(forms.ModelForm):
    repair_date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}), input_formats=['%Y-%m-%d'],
                                  label="Дата восстановления")
    failure_date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}), input_formats=['%Y-%m-%d'],
                                   label="Дата отказа")

    class Meta:
        model = Reclamation
        fields = [
            "vehicle",
            "failure_date",
            "operating_time",
            "failure_unit",
            "failure_description",
            "repair_procedure",
            "spare_parts",
            "repair_date",
        ]

        labels = {
            "vehicle": "Машина",
            "failure_date": "Дата отказа",
            "operating_time": "Наработка, м/час",
            "failure_unit": "Узел отказа",
            "failure_description": "Описание отказа",
            "repair_procedure": "Способ восстановления",
            "spare_parts": "Используемые запасные части",
            "repair_date": "Дата восстановления",
        }

        widgets = {
            'failure_description': forms.Textarea(attrs={"rows": "3", "cols": "40"}),
            'spare_parts': forms.Textarea(attrs={"rows": "3", "cols": "40"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs["initial"]["user"]
        service_deps = ServiceDepartment.objects.all()
        users_service_deps = []
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user in users_service_deps:
            self.fields["vehicle"] = forms.ModelChoiceField(
                queryset=Vehicle.objects.filter(service_department__user=user)
            )
            self.fields["vehicle"].label = "Машина"

    def clean(self):
        cleaned_data = super().clean()
        failure_date = cleaned_data.get("failure_date")
        repair_date = cleaned_data.get("repair_date")
        operating_time = cleaned_data.get("operating_time")
        if self.is_valid():
            if repair_date < failure_date:
                raise ValidationError({"repair_date": "Дата восстановления не может быть раньше Даты отказа!"})
            if operating_time < 0:
                raise ValidationError({"operating_time": "Время наработки не может быть отрицательным!"})
        return cleaned_data


class FlatPageForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        fields = "__all__"
