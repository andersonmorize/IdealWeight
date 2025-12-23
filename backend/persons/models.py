from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

from .validators import validate_cpf_numbers


class Person(models.Model):
    SEX_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[validate_cpf_numbers]
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    height = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        validators=[
            MinValueValidator(Decimal(0.50)), 
            MaxValueValidator(Decimal(2.50))]
    )
    weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[
            MinValueValidator(Decimal(2.00)),
            MaxValueValidator(Decimal(300.00))]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.cpf})"

    @property
    def ideal_weight(self):
        """
        Calcula o peso ideal baseado na fórmula:
        Homens: (72.7 * height) - 58
        Mulheres: (62.1 * height) - 44.7
        """
        height_float = float(self.height)
        
        if self.sex == 'M':
            ideal_weight = (72.7 * height_float) - 58
        else:
            ideal_weight = (62.1 * height_float) - 44.7
            
        return round(ideal_weight, 2)

