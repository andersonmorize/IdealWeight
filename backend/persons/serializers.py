import re

from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    ideal_weight = serializers.ReadOnlyField()

    class Meta:
        model = Person
        fields = [
            'id', 'name', 'date_of_birth', 'cpf', 
            'sex', 'height', 'weight', 'ideal_weight'
        ]

    def validate_cpf(self, value):
        """
        Validação básica de formato de CPF.
        Para produção, implementar algoritmo de dígito verificador.
        """
        clean_cpf = re.sub(r'[^0-9]', '', value)
        if len(clean_cpf) != 11:
            raise serializers.ValidationError("CPF deve conter 11 dígitos.")
        return value
