from django.db import models


class Vehiculo(models.Model):
    placa = models.CharField(
        max_length=7,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Placa o Matrícula"
    )
    marca = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name="Marca del Fabricante"
    )
    modelo = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name="Línea o Modelo"
    )
    anio_fabricacion = models.IntegerField(
        blank=False,
        null=False,
        verbose_name="Año de Fabricación"
    )
    kilometraje = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Kilometraje Acumulado (km)"
    )
    tarifa_diaria = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name="Tarifa de Alquiler por Día (USD)"
    )
    en_servicio = models.BooleanField(
        default=True,
        verbose_name="Disponible para Servicio"
    )
    ultimo_mantenimiento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha y Hora de Último Mantenimiento"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo} ({self.anio_fabricacion})"
