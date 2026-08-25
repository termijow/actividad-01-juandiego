# API REST - Sistema de Gestión de Flota Vehicular
**Estudiante:** Juan Diego  
**Asignatura:** Arquitectura de Software Moderna con Microservicios  
**Institución:** Corporación Universitaria Minuto de Dios — UNIMINUTO  
**Clase:** 02 — Monolito con Django: Arquitectura y CRUD  

---

## 1. Entidad y Dominio
- **Entidad principal:** `Vehiculo`
- **Descripción del dominio:** API REST para la administración y supervisión de la flota vehicular de una compañía de transporte y logística. Permite registrar, consultar, filtrar, actualizar y auditar unidades móviles según sus características técnicas (marca, modelo, año), métricas operativas (kilometraje acumulado, estado de servicio, último mantenimiento) e indicadores comerciales (tarifa diaria de alquiler).
- **Campo calculado (`estado_operativo`):** Campo dinámico derivado en el serializador que clasifica la unidad en `FUERA_DE_SERVICIO`, `ALERTA_REVISION_CRITICA` (>= 80,000 km), `MANTENIMIENTO_PREVENTIVO_SUGERIDO` (>= 40,000 km) u `OPTIMO_DISPONIBLE`.

---

## 2. Reglas de Negocio Implementadas en el Serializador
1. **Validación de Formato de Placa (`validate_placa`):** La placa debe cumplir con el formato alfanumérico estándar de 6 a 7 caracteres en mayúsculas (ej. `ABC-123` o `ABC123`). Se rechazan formatos incorrectos o con caracteres especiales prohibidos.
2. **Validación de Antigüedad de Flota (`validate_anio_fabricacion`):** Solo se admiten vehículos cuyo año de fabricación esté comprendido entre **2000 y 2027**, garantizando los estándares de seguridad vial y modernidad de la flota corporativa.
3. **Validación de Tarifa Comercial (`validate_tarifa_diaria`):** La tarifa diaria de alquiler debe ser estrictamente mayor a **$0.00 USD** y no puede exceder el límite corporativo fijado en **$5,000.00 USD**.

---

## 3. Endpoint Personalizado
- **Ruta:** `GET /api/vehiculos/mantenimiento_urgente/`
- **Relevancia y funcionamiento:** Retorna de forma estructurada todas las unidades vehiculares que requieren atención técnica urgente: aquellas que se encuentran fuera de servicio (`en_servicio=False`) o que han superado los **50,000 km** de recorrido (`kilometraje >= 50000`). La respuesta incluye el conteo total de unidades críticas y el detalle completo en formato JSON para el equipo de mecánicos y despachadores.

---

## 4. Instrucciones para Levantar el Proyecto en Local

### Opción A — Con Docker (Recomendado, 1 solo comando):
```bash
docker compose up --build
```
La API quedará disponible en `http://127.0.0.1:8000/api/vehiculos/`.

---

### Opción B — Con Entorno Virtual de Python:
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate && python manage.py runserver
```
