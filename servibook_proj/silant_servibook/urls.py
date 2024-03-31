from django.urls import path, include
from rest_framework.routers import DefaultRouter
from allauth.account.views import LoginView

from .views import *


router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicles')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')
router.register(r'reclamations', ReclamationViewSet, basename='reclamations')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/login/', LoginView.as_view(), name='account_login'),    
    path('', VehicleList.as_view(), name='vehicle_list'),
    path('maintenances/', MaintenanceList.as_view(), name='maintenance_list'),
    path('maintenances/<int:pk>', MaintenanceDetail.as_view(), name='maintenance_detail'),
    path('maintenances/create/', MaintenanceCreate.as_view(), name='maintenance_create'),
    path('maintenances/<int:pk>/update/', MaintenanceUpdate.as_view(), name='maintenance_update'),
    path('maintenances/<int:pk>/delete/', MaintenanceDelete.as_view(), name='maintenance_delete'),
    path('reclamations/', ReclamationList.as_view(), name='reclamation_list'),
    path('reclamations/<int:pk>', ReclamationDetail.as_view(), name='reclamation_detail'),
    path('reclamations/create/', ReclamationCreate.as_view(), name='reclamation_create'),
    path('reclamations/<int:pk>/update/', ReclamationUpdate.as_view(), name='reclamation_update'),
    path('reclamations/<int:pk>/delete/', ReclamationDelete.as_view(), name='reclamation_delete'),
    path('vehicles/<int:pk>', VehicleDetail.as_view(), name='vehicle_detail'),
    path('vehicles/create/', VehicleCreate.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/update/', VehicleUpdate.as_view(), name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', VehicleDelete.as_view(), name='vehicle_delete'),
    path('engines/<int:pk>', EngineDetail.as_view(), name='engine_detail'),
    path('transmissions/<int:pk>', TransmissionDetail.as_view(), name='transmission_detail'),
    path('drive_axles/<int:pk>', DriveAxleDetail.as_view(), name='drive_axle_detail'),
    path('steer_axles/<int:pk>', SteerAxleDetail.as_view(), name='steer_axle_detail'),
    path('clients/<int:pk>', ClientDetail.as_view(), name='client_detail'),
    path('service_departments/<int:pk>', ServiceDepartmentDetail.as_view(), name='service_department_detail'),
    path('machinery/<int:pk>', MachineryDetail.as_view(), name='machinery_detail'),
    path('clients/<int:pk>', ClientDetail.as_view(), name='client_detail'),
    path('service_deps_in_op/<int:pk>', ServiceDepInOperationDetail.as_view(), name='service_dep_in_op_detail'),
    path('maintenance_types/<int:pk>', MaintenanceTypeDetail.as_view(), name='maintenance_type_detail'),
    path('failure_units/<int:pk>', FailureUnitDetail.as_view(), name='failure_unit_detail'),
    path('repair_procedures/<int:pk>', RepairProcedureDetail.as_view(), name='repair_procedure_detail'),
]
