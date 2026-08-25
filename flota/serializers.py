import re
from rest_framework import serializers
from .models import Vehiculo


class VehiculoSerializer(serializers.ModelSerializer):
    estado_operativo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vehiculo
        fields = [
            'id',
            'placa',
            'marca',
            'modelo',
            'anio_fabricacion',
            'kilometraje',
            'tarifa_diaria',
            'en_servicio',
            'ultimo_mantenimiento',
            'estado_operativo',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_estado_operativo(self, obj) -> str:
        """
        Deriva el estado de alerta operativa de la unidad vehicular según su disponibilidad
        y kilometraje acumulado.
        """
        if not obj.en_servicio:
            return "FUERA_DE_SERVICIO"
        if float(obj.kilometraje) >= 80000:
            return "ALERTA_REVISION_CRITICA"
        if float(obj.kilometraje) >= 40000:
            return "MANTENIMIENTO_PREVENTIVO_SUGERIDO"
        return "OPTIMO_DISPONIBLE"

    def validate_placa(self, value):
        """
        Regla de negocio 1: La placa debe tener formato alfanumérico estándar
        de 6 a 7 caracteres en mayúsculas (ej: ABC-123 o ABC123).
        """
        placa_limpia = value.strip().upper()
        patron = r'^[A-Z0-9]{3}-?[A-Z0-9]{3}$'
        if not re.match(patron, placa_limpia):
            raise serializers.ValidationError(
                "La placa debe tener un formato válido de 6 a 7 caracteres alfanuméricos en mayúsculas (ej: ABC-123 o ABC123)."
            )
        return placa_limpia

    def validate_anio_fabricacion(self, value):
        """
        Regla de negocio 2: El año de fabricación debe estar entre 2000 y 2027.
        No se aceptan vehículos antiguos por políticas de seguridad vehicular.
        """
        if value < 2000 or value > 2027:
            raise serializers.ValidationError(
                "El año de fabricación debe estar comprendido entre el 2000 y el 2027 por políticas de modernización de flota."
            )
        return value

    def validate_tarifa_diaria(self, value):
        """
        Regla de negocio 3: La tarifa diaria debe ser un valor positivo mayor a 0
        y no superar los $5,000.00 USD.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "La tarifa diaria de alquiler debe ser estrictamente mayor a 0."
            )
        if value > 5000:
            raise serializers.ValidationError(
                "La tarifa diaria no puede superar el límite corporativo de $5,000.00 USD."
            )
        return value

    def validate_kilometraje(self, value):
        """
        Validación adicional: El kilometraje acumulado no puede ser un número negativo.
        """
        if value < 0:
            raise serializers.ValidationError(
                "El kilometraje acumulado no puede ser negativo."
            )
        return value
