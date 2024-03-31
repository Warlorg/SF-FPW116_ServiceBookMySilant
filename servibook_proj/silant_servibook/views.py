from rest_framework import viewsets
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import *
from .filters import *
from .permissions import *
from .forms import *
from .serializers import *


class VehicleList(ListView):
    model = Vehicle
    template_name = 'vehicles.html'
    context_object_name = 'vehicles'
    ordering = 'shipment_date'
    paginate_by = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            customers = Client.objects.all()
            service_deps = ServiceDepartment.objects.all()
            users_customers = []
            users_service_deps = []
            queryset = Vehicle.objects.all()
            for customer in customers:
                users_customers.append(customer.user)
            for service_dep in service_deps:
                users_service_deps.append(service_dep.user)
            if user.is_superuser == 1 or user.is_staff == 1:
                queryset = super().get_queryset()
            elif user in users_customers:
                queryset = Vehicle.objects.filter(customer__user=user).order_by('shipment_date')
            self.filter_set = VehicleFilter(self.request.GET, queryset)
        else:
            queryset = super().get_queryset()
            vehicle_number_param = self.request.GET.get('vehicle_number', '')
            if vehicle_number_param != '':
                queryset = queryset.filter(vehicle_number=vehicle_number_param)
            self.filter_set = VehicleSimpleFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_set'] = self.filter_set
        return context


class VehicleDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_vehicle"
    model = Vehicle
    template_name = "vehicle.html"
    context_object_name = "vehicle"

    def get_queryset(self):
        user = self.request.user
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        queryset = Vehicle.objects.none()
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_customers:
            queryset = Vehicle.objects.filter(customer__user=user)
        elif user in users_service_deps:
            queryset = Vehicle.objects.filter(service_dep__user=user)
        return queryset


class VehicleCreate(CreateView, PermissionRequiredMixin):
    permission_required = "silant_servibook.add_vehicle"
    form_class = VehicleForm
    model = Vehicle
    template_name = "vehicle_create.html"
    success_url = reverse_lazy("vehicle_list")


class VehicleUpdate(UpdateView, PermissionRequiredMixin):
    permission_required = "silant_servibook.change_vehicle"
    form_class = VehicleForm
    model = Vehicle
    template_name = "vehicle_create.html"
    success_url = reverse_lazy("vehicle_list")


class VehicleDelete(DeleteView, PermissionRequiredMixin):
    permission_required = "silant_servibook.delete_vehicle"
    model = Vehicle
    template_name = "vehicle_delete.html"
    success_url = reverse_lazy("vehicle_list")


class MaintenanceList(ListView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_maintenance"
    model = Maintenance
    template_name = "maintenances.html"
    ordering = "maintenance_date"
    context_object_name = "maintenances"
    paginate_by = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        queryset = Maintenance.objects.none()
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_customers:
            queryset = Maintenance.objects.filter(vehicle__customer__user=user).order_by("maintenance_date")
        elif user in users_service_deps:
            queryset = Maintenance.objects.filter(service_department__user=user).order_by("maintenance_date")
        self.filter_set = MaintenanceFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_set'] = self.filter_set
        return context


class MaintenanceDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_maintenance"
    model = Maintenance
    template_name = "maintenance.html"
    context_object_name = "maintenance"

    def get_queryset(self):
        user = self.request.user
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        queryset = Maintenance.objects.none()
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_customers:
            queryset = Maintenance.objects.filter(vehicle__customer__user=user)
        elif user in users_service_deps:
            queryset = Maintenance.objects.filter(service_dep__user=user)
        return queryset


class MaintenanceCreate(CreateView, PermissionRequiredMixin):
    permission_required = "silant_servibook.add_maintenance"
    model = Maintenance
    form_class = MaintenanceForm
    template_name = "maintenance_create.html"
    success_url = reverse_lazy("maintenance_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"]["user"] = self.request.user
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs


class MaintenanceUpdate(UpdateView, PermissionRequiredMixin):
    permission_required = "silant_servibook.change_maintenance"
    model = Maintenance
    form_class = MaintenanceForm
    template_name = "maintenance_create.html"
    success_url = reverse_lazy("maintenance_list")

    def get_queryset(self):
        user = self.request.user
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        queryset = Maintenance.objects.none()
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_customers:
            queryset = Maintenance.objects.filter(vehicle__customer__user=user)
        elif user in users_service_deps:
            queryset = Maintenance.objects.filter(service_dep__user=user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"]["user"] = self.request.user
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs


class MaintenanceDelete(DeleteView, PermissionRequiredMixin):
    permission_required = "silant_servibook.delete_maintenance"
    model = Maintenance
    template_name = "maintenance_delete.html"
    success_url = reverse_lazy("maintenance_list")

    def get_queryset(self):
        user = self.request.user
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        queryset = Maintenance.objects.none()
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_customers:
            queryset = Maintenance.objects.filter(vehicle__customer__user=user)
        elif user in users_service_deps:
            queryset = Maintenance.objects.filter(service_dep__user=user)
        return queryset


class ReclamationList(ListView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_reclamation"
    model = Reclamation
    template_name = "reclamations.html"
    ordering = "failure_date"
    context_object_name = "reclamations"
    paginate_by = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        queryset = Reclamation.objects.none()
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_customers:
            queryset = Reclamation.objects.filter(vehicle__customer__user=user).order_by("failure_date")
        elif user in users_service_deps:
            queryset = Reclamation.objects.filter(service_dep__user=user).order_by("failure_date")
        self.filter_set = ReclamationFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_set'] = self.filter_set
        return context


class ReclamationDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_reclamation"
    model = Reclamation
    template_name = "reclamation.html"
    context_object_name = "reclamation"

    def get_queryset(self):
        user = self.request.user
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        queryset = Reclamation.objects.none()
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_customers:
            queryset = Reclamation.objects.filter(vehicle__customer__user=user)
        elif user in users_service_deps:
            queryset = Reclamation.objects.filter(service_dep__user=user)
        return queryset


class ReclamationCreate(CreateView, PermissionRequiredMixin):
    permission_required = "silant_servibook.add_reclamation"
    model = Reclamation
    form_class = ReclamationForm
    template_name = "reclamation_create.html"
    success_url = reverse_lazy("reclamation_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"]["user"] = self.request.user
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs


class ReclamationUpdate(UpdateView, PermissionRequiredMixin):
    permission_required = "silant_servibook.change_reclamation"
    model = Reclamation
    form_class = ReclamationForm
    template_name = "reclamation_create.html"
    success_url = reverse_lazy("reclamation_list")

    def get_queryset(self):
        user = self.request.user
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        queryset = Reclamation.objects.none()
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_customers:
            queryset = Reclamation.objects.filter(vehicle__customer__user=user)
        elif user in users_service_deps:
            queryset = Reclamation.objects.filter(service_dep__user=user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"]["user"] = self.request.user
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs


class ReclamationDelete(DeleteView, PermissionRequiredMixin):
    permission_required = "silant_servibook.delete_reclamation"
    model = Reclamation
    template_name = "reclamation_delete.html"
    success_url = reverse_lazy("reclamation_list")

    def get_queryset(self):
        user = self.request.user
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        queryset = Reclamation.objects.none()
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_customers:
            queryset = Reclamation.objects.filter(vehicle__customer__user=user)
        elif user in users_service_deps:
            queryset = Reclamation.objects.filter(service_dep__user=user)
        return queryset


class MachineryDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_machine"
    model = Machinery
    template_name = "information.html"
    context_object_name = "information"


class EngineDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_engine"
    model = Engine
    template_name = "information.html"
    context_object_name = "information"


class TransmissionDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_transmission"
    model = Transmission
    template_name = "information.html"
    context_object_name = "information"


class DriveAxleDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_driveAxle"
    model = DriveAxle
    template_name = "information.html"
    context_object_name = "information"


class SteerAxleDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_steerAxle"
    model = SteerAxle
    template_name = "information.html"
    context_object_name = "information"


class ClientDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_client"
    model = Client
    template_name = "information.html"
    context_object_name = "information"


class ServiceDepartmentDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_serviceDepartment"
    model = ServiceDepartment
    template_name = "information.html"
    context_object_name = "information"


class ServiceDepInOperationDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_serviceDepInOperation"
    model = ServiceDepInOperation
    template_name = "information.html"
    context_object_name = "information"


class MaintenanceTypeDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_maintenanceType"
    model = MaintenanceType
    template_name = "information.html"
    context_object_name = "information"


class FailureUnitDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_failureUnit"
    model = FailureUnit
    template_name = "information.html"
    context_object_name = "information"


class RepairProcedureDetail(DetailView, PermissionRequiredMixin):
    permission_required = "silant_servibook.view_repairProcedure"
    model = RepairProcedure
    template_name = "information.html"
    context_object_name = "information"


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            customers = Client.objects.all()
            service_deps = ServiceDepartment.objects.all()
            users_customers = []
            users_service_deps = []
            queryset = Vehicle.objects.none()
            for customer in customers:
                users_customers.append(customer.user)
            for service_dep in service_deps:
                users_service_deps.append(service_dep.user)
            if user.is_superuser == 1 or user.is_staff == 1:
                queryset = super().get_queryset()
            elif user in users_customers:
                queryset = Vehicle.objects.filter(customer__user=user).order_by("shipment_date")
            elif user in users_service_deps:
                queryset = Vehicle.objects.filter(service_dep__user=user).order_by("shipment_date")
            self.filter_set = VehicleFilter(self.request.GET, queryset)
        else:
            if not self.request.GET.__contains__('vehicle_number'):
                super().get_queryset()
                queryset = Vehicle.objects.none()
            else:
                if self.request.GET.get('vehicle_number') != '':
                    queryset = super().get_queryset()
                else:
                    super().get_queryset()
                    queryset = Vehicle.objects.none()
                self.filter_set = VehicleSimpleFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrManagerOrClientOrServiceDepartment()]
        else:
            return [IsAdminOrManager()]


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        queryset = Maintenance.objects.none()
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_customers:
            queryset = Maintenance.objects.filter(customer__user=user).order_by("maintenance_date")
        elif user in users_service_deps:
            queryset = Maintenance.objects.filter(service_dep__user=user).order_by("maintenance_date")
        self.filter_set = MaintenanceFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrManagerOrClientOrServiceDepartment()]
        else:
            return [IsAdminOrManager()]


class ReclamationViewSet(viewsets.ModelViewSet):
    queryset = Reclamation.objects.all()
    serializer_class = ReclamationSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_set = None

    def get_queryset(self):
        user = self.request.user
        customers = Client.objects.all()
        service_deps = ServiceDepartment.objects.all()
        users_customers = []
        users_service_deps = []
        queryset = Reclamation.objects.none()
        for customer in customers:
            users_customers.append(customer.user)
        for service_dep in service_deps:
            users_service_deps.append(service_dep.user)
        if user.is_superuser == 1 or user.is_staff == 1:
            queryset = super().get_queryset()
        elif user in users_customers:
            queryset = Reclamation.objects.filter(customer__user=user).order_by("failure_date")
        elif user in users_service_deps:
            queryset = Reclamation.objects.filter(service_dep__user=user).order_by("failure_date")
        self.filter_set = ReclamationFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrManagerOrClientOrServiceDepartment()]
        else:
            return [IsAdminOrManager()]
