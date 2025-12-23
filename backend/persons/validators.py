import re
from django.core.exceptions import ValidationError

def validate_cpf_numbers(value):
    cpf = re.sub(r'[^0-9]', '', str(value))

    if len(cpf) != 11:
        raise ValidationError("O CPF deve conter exatamente 11 dígitos numéricos.")

    if cpf in [s * 11 for s in [str(n) for n in range(10)]]:
        raise ValidationError("CPF inválido.")

    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(i)))
        digit = ((value * 10) % 11) % 10
        if digit != int(cpf[i]):
            raise ValidationError("CPF inválido.")
    
    return cpf

