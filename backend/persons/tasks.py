from django.db.models import Q
from .models import Person


class PersonTask:
    """
    Classe Task: Responsável pela interação direta com o ORM Django.
    """
    @staticmethod
    def create(data):
        return Person.objects.create(**data)

    @staticmethod
    def update(person_id, data):
        person = Person.objects.get(pk=person_id)
        for attr, value in data.items():
            setattr(person, attr, value)
        person.save()
        return person

    @staticmethod
    def delete(person_id):
        person = Person.objects.get(pk=person_id)
        person.delete()

    @staticmethod
    def get_by_id(person_id):
        return Person.objects.get(pk=person_id)

    @staticmethod
    def filter_people(filters, search_term=None):
        queryset = Person.objects.filter(**filters)
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) | Q(cpf=search_term)
            )
        return queryset
