import django_filters
from django_filters import FilterSet, ModelChoiceFilter
from .models import *


class VehicleFilter(FilterSet):
    vehicle_model = ModelChoiceFilter(
        field_name="vehicle_model__title",
        queryset=Machinery.objects.all(),
        label="Модель техники",
    )

    engine_model = ModelChoiceFilter(
        field_name="engine_model__title",
        queryset=Engine.objects.all(),
        label="Модель двигателя",
    )

    transmission_model = ModelChoiceFilter(
        field_name="transmission_model__title",
        queryset=Transmission.objects.all(),
        label="Модель трансмиссии",
    )

    drive_axle_model = ModelChoiceFilter(
        field_name="drive_axle_model__title",
        queryset=DriveAxle.objects.all(),
        label="Модель ведущего моста",
    )

    steer_axle_model = ModelChoiceFilter(
        field_name="steer_axle_model__title",
        queryset=SteerAxle.objects.all(),
        label="Модель управляемого моста",
    )


class VehicleSimpleFilter(FilterSet):
    vehicle_number = django_filters.CharFilter(
        field_name="vehicle_number",
        lookup_expr="icontains",
        label="Заводской № машины",
    )


class MaintenanceFilter(FilterSet):
    vehicle = django_filters.CharFilter(
        field_name="vehicle__vehicle_number",
        lookup_expr="icontains",
        label="Заводской № машины",
    )

    type = ModelChoiceFilter(
        field_name="type__title",
        queryset=MaintenanceType.objects.all(),
        label="Вид ТО",
    )    

    service_department = ModelChoiceFilter(
        field_name="service_department__title",
        queryset=ServiceDepartment.objects.all(),
        label="Сервисная компания"
    )


class ReclamationFilter(FilterSet):
    failure_unit = ModelChoiceFilter(
        field_name="failure_unit__title",
        queryset=FailureUnit.objects.all(),
        label="Узел отказа"
    )

    repair_procedure = ModelChoiceFilter(
        field_name="repair_procedure__title",
        queryset=RepairProcedure.objects.all(),
        label="Способ восстановления",
    )

    service_department = ModelChoiceFilter(
        field_name="service_department__title",
        queryset=ServiceDepartment.objects.all(),
        label="Сервисная компания"
    )
