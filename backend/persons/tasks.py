import csv
import io
from celery import shared_task
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
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


@shared_task(bind=True)
def import_persons_from_csv(self, file_content):
    stream = io.StringIO(file_content)
    reader = csv.DictReader(stream)
    
    success_count = 0
    errors = []

    for index, row in enumerate(reader):
        try:
            # 1. Validação Manual de Negócio (ex: CPF)
            cpf = row.get('cpf', '').strip()
            validate_cpf_numbers(cpf)
            
            # 2. Preparação da instância (sem salvar ainda)
            person = Person(
                name=row['name'],
                date_of_birth=row['date_of_birth'],
                cpf=cpf,
                sex=row['sex'],
                height=row['height'],
                weight=row['weight']
            )
            
            # 3. Validação completa do Model (checa campos, escolhas e constraints)
            person.full_clean() 
            person.save()
            success_count += 1
            
        except ValidationError as e:
            errors.append(f"Linha {index + 1} ({row.get('name')}): {e.messages}")
        except Exception as e:
            errors.append(f"Linha {index + 1}: Erro inesperado: {str(e)}")

    return {
        "status": "completed",
        "created": success_count,
        "errors": errors
    }

@shared_task
def export_persons_to_csv():
    # 1. Busca os dados
    people = Person.objects.all()
    
    # 2. Cria o arquivo CSV em memória
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Nome', 'Data de Nascimento', 'CPF', 'Sexo', 'Altura', 'Peso', 'Peso Ideal'])
    
    for person in people:
        writer.writerow([
            person.name,
            person.date_of_birth,
            person.cpf,
            person.get_sex_display(),
            person.height,
            person.weight,
            person.ideal_weight  # Usando a property do Model
        ])
    
    # 3. Salva o arquivo em um local temporário (ex: media/exports/)
    filename = f"exports/pessoas_exportadas.csv"
    file_content = ContentFile(output.getvalue().encode('utf-8'))
    path = default_storage.save(filename, file_content)
    
    return {"file_url": path}