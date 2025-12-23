from django.contrib import admin
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'date_of_birth', 'cpf', 
        'sex', 'height', 'weight', 'ideal_weight')
    
    search_fields = ('name', 'cpf')
    
    list_filter = ('sex',)

    readonly_fields = ('ideal_weight',)
