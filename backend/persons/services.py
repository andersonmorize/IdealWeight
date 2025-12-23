from .tasks import PersonTask


class PersonService:
    """
    Classe Service: Atua entre o Controller e a Task.
    """
    @staticmethod
    def handle_create(dto_data):
        return PersonTask.create(dto_data)

    @staticmethod
    def handle_update(person_id, dto_data):
        return PersonTask.update(person_id, dto_data)

    @staticmethod
    def handle_delete(person_id):
        return PersonTask.delete(person_id)

    @staticmethod
    def handle_search(filters):
        return PersonTask.filter_people(filters)

    @staticmethod
    def get_person_by_id(person_id):
        return PersonTask.get_by_id(person_id)

    @staticmethod
    def get_ideal_weight_calculation(person_id):
        """
        Lógica para o ponto extra solicitada na prova.
        """
        person = PersonTask.get_by_id(person_id)
        altura = float(person.height)
        
        # Fórmulas exigidas: Homem: (72.7 * altura) - 58 | Mulher: (62.1 * altura) - 44.7
        if person.sex == 'M':
            peso_ideal = (72.7 * altura) - 58
        else:
            peso_ideal = (62.1 * altura) - 44.7
            
        return round(peso_ideal, 2)
