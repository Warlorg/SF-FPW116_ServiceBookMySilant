from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from .forms import FlatPageForm
from .models import *


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('get_user_groups', )

    def get_user_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_user_groups.short_description = 'Группа'


class MachineryAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


class EngineAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


class TransmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


class DriveAxleAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


class SteerAxleAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


class ServiceDepartmentAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


class ServiceDepInOperationAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


class MaintenanceTypeAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


class FailureUnitAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


class RepairProcedureAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


class ClientAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "user")


class VehicleAdmin(admin.ModelAdmin):
    list_display = ("vehicle_model", "vehicle_number", "engine_model", "engine_number", "transmission_model",
                    "transmission_number", "drive_axle_model", "drive_axle_number", "steer_axle_model",
                    "steer_axle_number", "delivery_contract", "shipment_date", "customer", "end_user",
                    "shipping_address", "configuration", "service_department")


class CustomFlatPageAdmin(FlatPageAdmin):
    form = FlatPageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)
admin.site.register(Machinery, MachineryAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(Transmission, TransmissionAdmin)
admin.site.register(DriveAxle, DriveAxleAdmin)
admin.site.register(SteerAxle, SteerAxleAdmin)
admin.site.register(ServiceDepartment, ServiceDepartmentAdmin)
admin.site.register(ServiceDepInOperation, ServiceDepInOperationAdmin)
admin.site.register(MaintenanceType, MaintenanceTypeAdmin)
admin.site.register(FailureUnit, FailureUnitAdmin)
admin.site.register(RepairProcedure, RepairProcedureAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Reclamation, ReclamationAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
