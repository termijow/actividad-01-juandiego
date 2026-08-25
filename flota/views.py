from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Vehiculo
from .serializers import VehiculoSerializer


class VehiculoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la gestión completa (CRUD) de la flota vehicular.
    Permite búsqueda por texto, ordenamiento y consulta de unidades críticas.
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Búsqueda sobre 3 campos de texto
    search_fields = ['placa', 'marca', 'modelo']
    
    # Ordenamiento sobre 4 campos numéricos y de fecha
    ordering_fields = ['anio_fabricacion', 'kilometraje', 'tarifa_diaria', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'], url_path='mantenimiento_urgente')
    def mantenimiento_urgente(self, request):
        """
        Endpoint personalizado que retorna las unidades que requieren intervención
        técnica urgente (fuera de servicio o con kilometraje >= 50,000 km).
        """
        vehiculos_urgentes = self.get_queryset().filter(
            Q(en_servicio=False) | Q(kilometraje__gte=50000)
        )
        serializer = self.get_serializer(vehiculos_urgentes, many=True)
        return Response(
            {
                "total_urgentes": vehiculos_urgentes.count(),
                "criterio": "Unidades fuera de servicio (en_servicio=False) o con kilometraje >= 50,000 km",
                "resultados": serializer.data
            },
            status=status.HTTP_200_OK
        )
