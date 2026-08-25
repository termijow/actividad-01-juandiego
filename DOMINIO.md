# Mi dominio

**Entidad principal:** Vehiculo

**Descripción:** Representa un vehículo perteneciente a la flota de transporte y logística de una empresa de alquiler y distribución. Modela las características técnicas, operativas y comerciales de cada unidad móvil, permitiendo monitorear su disponibilidad, kilometraje acumulado, tarifas y estado de mantenimiento preventivo y correctivo en tiempo real.

**Campos:**

| Campo | Tipo Django | Restricciones de negocio |
|---|---|---|
| `placa` | CharField | `max_length=7`, `unique=True`, `blank=False`. Debe tener formato estándar de 6 a 7 caracteres alfanuméricos en mayúsculas (ej. ABC-123 o ABC123). |
| `marca` | CharField | `max_length=50`, `blank=False`. Nombre del fabricante automotriz (mínimo 2 caracteres). |
| `modelo` | CharField | `max_length=50`, `blank=False`. Línea o modelo comercial del vehículo. |
| `anio_fabricacion` | IntegerField | `blank=False`. Año de fabricación del vehículo. No puede ser anterior al año 2000 ni superior al año en curso + 1. |
| `kilometraje` | DecimalField | `max_digits=10`, `decimal_places=2`, `default=0.00`. Kilometraje recorrido acumulado; no puede ser un valor negativo. |
| `tarifa_diaria` | DecimalField | `max_digits=8`, `decimal_places=2`, `blank=False`. Precio diario de alquiler en USD; debe ser estrictamente mayor a 0 y menor a $5,000.00. |
| `en_servicio` | BooleanField | `default=True`. Indica si el vehículo está operativo y apto para ser despachado o si se encuentra temporalmente fuera de servicio. |
| `ultimo_mantenimiento` | DateTimeField | `null=True`, `blank=True`. Fecha y hora del último mantenimiento técnico registrado. |
| `created_at` | DateTimeField | `auto_now_add=True`. Fecha y hora de creación del registro en el sistema (auditoría). |

**Reglas de negocio:**

1. **Validación de formato de placa (`validate_placa`):** La placa debe ser una cadena válida de 6 a 7 caracteres alfanuméricos en mayúsculas (letras mayúsculas y números, opcionalmente separados por un único guión central), sin caracteres especiales no permitidos ni espacios.
2. **Validación de antigüedad de flota (`validate_anio_fabricacion`):** Por políticas de seguridad y modernidad de la flota, solo se aceptan vehículos fabricados entre el año 2000 y el año futuro inmediato (2027). No se admiten modelos más antiguos.
3. **Validación de tarifa comercial (`validate_tarifa_diaria`):** La tarifa diaria de alquiler debe ser un monto positivo mayor a $0.00 USD y no puede exceder el límite comercial corporativo fijado en $5,000.00 USD por día.

**Endpoint personalizado que voy a agregar:** `GET /api/vehiculos/mantenimiento_urgente/`

**Qué hace ese endpoint:** Filtra y lista de manera estructurada todos los vehículos de la flota que requieren intervención mecánica prioritaria: aquellos que se encuentran marcados como fuera de servicio (`en_servicio=False`) o aquellos cuyo kilometraje acumulado ha superado los 50,000 km (`kilometraje >= 50000`). Retorna un objeto JSON con el conteo total de vehículos críticos y la lista detallada de unidades.
