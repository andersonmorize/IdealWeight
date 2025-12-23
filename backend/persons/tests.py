import re
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker

from .models import Person

class PersonAPITests(APITestCase):
    def setUp(self):
        self.fake = Faker('pt_BR')
        self.base_cpf = self.fake.cpf()
        self.person_data = {
            "name": "John Doe",
            "date_of_birth": "1990-05-15",
            "cpf": self.base_cpf,
            "sex": "M",
            "height": 1.80,
            "weight": 85.00
        }
        self.person = Person.objects.create(**self.person_data)
        self.url = reverse('person-list')

    def test_create_person(self):
        """Test if we can create a new person and if ideal weight is calculated"""
        data = {
            "name": "Jane Doe",
            "date_of_birth": "1995-10-20",
            "cpf": "98765432100",
            "sex": "F",
            "height": 1.60,
            "weight": 60.00
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if ideal weight for Female is correct: (62.1 * 1.6) - 44.7 = 54.66
        self.assertEqual(float(response.data['ideal_weight']), 54.66)

    def test_list_persons(self):
        """Testa se a listagem de pessoas funciona"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_by_cpf(self):
        """Testa a funcionalidade de busca (Requisito: Pesquisar) """
        url = f"{self.url}?cpf={self.base_cpf}" 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['cpf'], self.base_cpf)

    def test_update_person(self):
        """Testa a alteração do peso (Requisito: Alterar) """
        detail_url = reverse('person-detail', args=[self.person.id])
        
        updated_data = {
            "name": self.person.name,
            "date_of_birth": self.person.date_of_birth,
            "cpf": self.person.cpf,
            "sex": self.person.sex,
            "height": str(self.person.height),
            "weight": 82.00
        }
        
        response = self.client.put(detail_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.person.refresh_from_db()
        self.assertEqual(float(self.person.weight), 82.00)

    def test_delete_person(self):
        """Test person removal"""
        detail_url = reverse('person-detail', args=[self.person.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)

    def test_create_person_invalid_cpf_format(self):
        """Testa se o sistema rejeita CPFs com tamanho errado ou letras"""
        data = self.person_data.copy()
        data["cpf"] = "123.456.789-0A"
        data["name"] = "Invalid CPF User"
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cpf', response.data)

    def test_create_person_invalid_cpf_checksum(self):
        """Testa se o sistema rejeita um CPF que tem 11 dígitos mas é matematicamente inválido"""
        data = self.person_data.copy()
        data["cpf"] = "11122233344"
        data["name"] = "Fake CPF User"
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['cpf'][0], "CPF inválido.")

    def test_create_person_with_formatted_cpf_success(self):
        """Testa se o sistema aceita CPF formatado mas limpa e salva apenas números"""
        
        # O Faker gera um CPF formatado válido(ex: 123.456.789-01)
        valid_cpf_formatted = self.fake.cpf()
        # Extraímos apenas os números para a comparação final
        expected_clean_cpf = re.sub(r'[^0-9]', '', valid_cpf_formatted)

        data = self.person_data.copy()
        data["cpf"] = valid_cpf_formatted
        data["name"] = "Formatted User"
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        person = Person.objects.get(name="Formatted User")
        self.assertEqual(person.cpf, expected_clean_cpf)
        self.assertEqual(len(person.cpf), 11)

    def test_height_weight_validators(self):
        """Testa os validadores de valor mínimo e máximo para altura e peso"""
        data = self.person_data.copy()
        data["cpf"] = "53820241036"
        data["height"] = 3.00
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('height', response.data)

    def test_ideal_weight_calculation_male(self):
        """Garante que o cálculo do peso ideal masculino está matematicamente correto"""
        # (72.7 * 1.80) - 58 = 130.86 - 58 = 72.86
        detail_url = reverse('person-detail', args=[self.person.id])
        response = self.client.get(detail_url)
        
        self.assertEqual(float(response.data['ideal_weight']), 72.86)

    def test_search_by_name_partial(self):
        """Testa se a pesquisa encontra uma pessoa por parte do nome (icontains)"""
        # Criamos uma pessoa específica para este teste
        Person.objects.create(
            name="Alice Wonder",
            date_of_birth="1992-01-01",
            cpf="11122233344",
            sex="F",
            height=1.70,
            weight=65.00
        )
        
        # Pesquisamos apenas por "Wonder"
        response = self.client.get(self.url, {'search': 'Wonder'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Alice Wonder")

    def test_search_by_cpf_exact(self):
        """Testa se a pesquisa encontra uma pessoa pelo CPF exato"""
        target_cpf = "55566677788"
        Person.objects.create(
            name="Bob Searcher",
            date_of_birth="1985-03-10",
            cpf=target_cpf,
            sex="M",
            height=1.75,
            weight=80.00
        )
        
        response = self.client.get(self.url, {'search': target_cpf}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['cpf'], target_cpf)

    def test_search_no_results(self):
        """Testa se retorna lista vazia quando nenhum critério é satisfeito"""
        response = self.client.get(self.url, {'search': 'Inexistente'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
