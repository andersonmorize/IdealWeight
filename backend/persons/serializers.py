import re

from rest_framework import serializers
from .models import Person
from .validators import validate_cpf_numbers


class PersonSerializer(serializers.ModelSerializer):
    ideal_weight = serializers.ReadOnlyField()

    class Meta:
        model = Person
        fields = [
            'id', 'name', 'date_of_birth', 'cpf', 
            'sex', 'height', 'weight', 'ideal_weight'
        ]

    def validate_cpf(self, value):
        clean_cpf = re.sub(r'[^0-9]', '', str(value))
        validate_cpf_numbers(clean_cpf)
        return clean_cpf

