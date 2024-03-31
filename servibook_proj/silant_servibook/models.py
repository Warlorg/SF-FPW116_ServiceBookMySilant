from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Machinery(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, default="Модель техники", verbose_name="Описание")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Модель техники"
        verbose_name_plural = "Модель техники"


class Engine(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, default="Модель двигателя", verbose_name="Описание")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Модель двигателя"
        verbose_name_plural = "Модель двигателей"


class Transmission(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, default="Модель трансмиссии", verbose_name="Описание")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Модель трансмиссии"
        verbose_name_plural = "Модель трансмиссий"


class DriveAxle(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, default="Модель ведущего моста", verbose_name="Описание")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Модель ведущего моста"
        verbose_name_plural = "Модель ведущих мостов"


class SteerAxle(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, default="Модель управляемого моста", verbose_name="Описание")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Модель управляемого моста"
        verbose_name_plural = "Модель управляемых мостов"


class ServiceDepartment(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, default="Сервисная компания", verbose_name="Описание")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Сервисная компания"
        verbose_name_plural = "Сервисные компании"


class ServiceDepInOperation(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, default="Организация, проводившая ТО", verbose_name="Описание")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Организация, проводившая ТО"
        verbose_name_plural = "Организации, проводившие ТО"


class MaintenanceType(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, default="Вид ТО", verbose_name="Описание")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Вид ТО"
        verbose_name_plural = "Виды ТО"


class FailureUnit(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, default="Узел отказа", verbose_name="Описание")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Узел отказа"
        verbose_name_plural = "Узлы отказа"


class RepairProcedure(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, default="Способ восстановления", verbose_name="Описание")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Способ восстановления"
        verbose_name_plural = "Способы восстановления"


class Client(models.Model):
    objects = None
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, default="Клиент", verbose_name="Описание")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Vehicle(models.Model):
    objects = None
    vehicle_model = models.ForeignKey(Machinery, on_delete=models.CASCADE, verbose_name="Модель техники",
                                      related_name="vehicle_machinery")
    vehicle_number = models.CharField(unique=True, max_length=255, verbose_name="Заводской № машины")
    engine_model = models.ForeignKey(Engine, on_delete=models.CASCADE, verbose_name="Модель двигателя",
                                     related_name="vehicle_engine")
    engine_number = models.CharField(unique=True, max_length=255, verbose_name="Заводской № двигателя")
    transmission_model = models.ForeignKey(Transmission, on_delete=models.CASCADE, verbose_name="Модель трансмиссии")
    transmission_number = models.CharField(unique=True, max_length=255, verbose_name="Заводской № трансмиссии")
    drive_axle_model = models.ForeignKey(DriveAxle, on_delete=models.CASCADE, verbose_name="Модель ведущего моста")
    drive_axle_number = models.CharField(max_length=255, verbose_name="Заводской № ведущего моста")
    steer_axle_model = models.ForeignKey(SteerAxle, on_delete=models.CASCADE, verbose_name="Модель управляемого моста")
    steer_axle_number = models.CharField(max_length=255, verbose_name="Заводской № управляемого моста")
    delivery_contract = models.CharField(max_length=255, verbose_name="Договор поставки (№, дата)")
    shipment_date = models.DateField(max_length=50, verbose_name="Дата отгрузки с завода")
    customer = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Покупатель")
    end_user = models.CharField(max_length=255, verbose_name="Грузополучатель (конечный потребитель)")
    shipping_address = models.CharField(max_length=255, verbose_name="Адрес поставки (эксплуатации)")
    configuration = models.TextField(max_length=1000, default="Стандарт", verbose_name="Комплектация (доп. опции)")
    service_department = models.ForeignKey(ServiceDepartment, on_delete=models.CASCADE,
                                           verbose_name="Сервисная компания")

    def __str__(self):
        return f'{self.vehicle_number}'

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"


class Maintenance(models.Model):
    objects = None
    type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE, verbose_name="Вид ТО")
    maintenance_date = models.DateField(max_length=50, verbose_name="Дата проведения ТО")
    operating_time = models.IntegerField(default=0, verbose_name="Наработка, м/час")
    order_number = models.CharField(max_length=255, verbose_name="Номер заказ-наряда")
    order_date = models.DateField(max_length=50, verbose_name="Дата заказ-наряда")
    maintenance_service = models.ForeignKey(ServiceDepInOperation, on_delete=models.CASCADE,
                                            verbose_name="Организация, проводившая ТО")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="Машина")
    service_department = models.ForeignKey(ServiceDepartment, on_delete=models.CASCADE,
                                           verbose_name="Сервисная компания")

    def save(self, *args, **kwargs):
        self.service_department = self.vehicle.service_department
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.vehicle} - {self.type} - {self.maintenance_date}'

    class Meta:
        verbose_name = "Техническое обслуживание"
        verbose_name_plural = "Технические обслуживания"


class Reclamation(models.Model):
    objects = None
    failure_date = models.DateField(verbose_name="Дата отказа")
    operating_time = models.IntegerField(default=0, verbose_name="Наработка, м/час")
    failure_unit = models.ForeignKey(FailureUnit, on_delete=models.CASCADE, verbose_name="Узел отказа")
    failure_description = models.TextField(max_length=1000, verbose_name="Описание отказа")
    repair_procedure = models.ForeignKey(RepairProcedure, on_delete=models.CASCADE,
                                         verbose_name="Способ восстановления")
    spare_parts = models.TextField(max_length=1000, blank=True, verbose_name="Используемые запасные части")
    repair_date = models.DateField(max_length=50, verbose_name="Дата восстановления")
    nonuse_time = models.IntegerField(default=0, verbose_name="Время простоя техники")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="Машина")
    service_department = models.ForeignKey(ServiceDepartment, on_delete=models.CASCADE,
                                           verbose_name="Сервисная компания")

    def save(self, *args, **kwargs):
        self.nonuse_time = (self.repair_date - self.failure_date).days
        self.service_department = self.vehicle.service_department
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.vehicle} - {self.failure_date} - {self.failure_unit}'

    class Meta:
        verbose_name = "Рекламация"
        verbose_name_plural = "Рекламации"


class MaintenanceAdmin(admin.ModelAdmin):
    exclude = ["service_department"]


class ReclamationAdmin(admin.ModelAdmin):
    exclude = ["nonuse_time", "service_department"]
