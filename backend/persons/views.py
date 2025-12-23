from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .models import Person
from .serializers import PersonSerializer
from .services import PersonService

class PersonViewSet(viewsets.ViewSet):
    """
    Controller que gerencia as requisições REST para a entidade Pessoa.
    Segue a hierarquia: Controller -> Service -> Task.
    """
    
    lookup_field = 'id'

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def list(self, request):
        search_query = request.query_params.get('search')
        
        people = PersonService.handle_search(filters={}, search_term=search_query)
        
        serializer = PersonSerializer(people, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, id=None):
        """
        Operação: Obter Detalhes
        """
        try:
            # Controller chama Service
            person = PersonService.get_person_by_id(id)
            serializer = PersonSerializer(person)
            return Response(serializer.data)
        except Person.DoesNotExist:
            return Response(
                {"detail": "Pessoa não encontrada."}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        """
        Operação: Incluir
        Recebe JSON, valida no DTO (Serializer) e envia para Service.
        """
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            person = PersonService.handle_create(serializer.validated_data)
            return Response(PersonSerializer(person).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id=None):
        """
        Operação: Alterar
        """
        try:
            person_instance = PersonService.get_person_by_id(id)
        except Person.DoesNotExist:
            return Response({"detail": "Não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonSerializer(instance=person_instance, data=request.data)
        
        if serializer.is_valid():
            person = PersonService.handle_update(id, serializer.validated_data)
            return Response(PersonSerializer(person).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id=None):
        """
        Operação: Excluir
        """
        PersonService.handle_delete(id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def calculate_ideal_weight(self, request, id=None):
        """
        Ponto Extra: Cálculo do peso ideal via Server. 
        Retorna o valor para ser exibido em um popup no Client.
        """
        result = PersonService.get_ideal_weight_calculation(id)
        return Response({'ideal_weight': result}, status=status.HTTP_200_OK)
