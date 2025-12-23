from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Person

class PersonAPITests(APITestCase):
    def setUp(self):
        # Criando um registro inicial para testes de detalhe/edição
        self.person_data = {
            "name": "John Doe",
            "date_of_birth": "1990-05-15",
            "cpf": "12345678901",
            "sex": "M",
            "height": 1.80,
            "weight": 85.00
        }
        self.person = Person.objects.create(**self.person_data)
        self.url = reverse('person-list') # Ajuste se o nome da rota no router for diferente

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
        """Test if listing persons works"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_by_cpf(self):
        """Test the search functionality (Requirement: Pesquisar)"""
        url = f"{self.url}?search=12345678901"
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['cpf'], "12345678901")

    def test_update_person(self):
        """Test updating person's weight"""
        detail_url = reverse('person-detail', args=[self.person.id])
        updated_data = {"weight": 82.00}
        response = self.client.patch(detail_url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.person.refresh_from_db()
        self.assertEqual(float(self.person.weight), 82.00)

    def test_delete_person(self):
        """Test person removal"""
        detail_url = reverse('person-detail', args=[self.person.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)

