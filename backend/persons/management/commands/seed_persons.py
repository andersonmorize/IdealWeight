import random
from django.core.management.base import BaseCommand
from faker import Faker
from persons.models import Person 

class Command(BaseCommand):
    help = 'Gera dados falsos para o modelo Person'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            type=int,
            default=10,
            help='Número de pessoas a serem criadas'
        )

    def handle(self, *args, **options):
        fake = Faker(['pt_BR'])
        number = options['number']

        self.stdout.write(f'Gerando {number} pessoas...')

        for _ in range(number):
            sex = random.choice(['M', 'F'])
            
            if sex == 'M':
                name = fake.name_male()
            else:
                name = fake.name_female()

            cpf = fake.cpf()
            cpf = cpf.replace('.', '').replace('-', '')

            Person.objects.create(
                name=name,
                date_of_birth=fake.date_of_birth(minimum_age=10, maximum_age=90),
                cpf=cpf,
                sex=sex,
                height=round(random.uniform(1.50, 2.00), 2),
                weight=round(random.uniform(50.00, 110.00), 2)
            )

        self.stdout.write(self.style.SUCCESS(f'Sucesso! {number} pessoas criadas.'))