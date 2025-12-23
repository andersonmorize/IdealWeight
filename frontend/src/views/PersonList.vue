<template>
  <v-container>
    <v-card class="mb-4">
      <v-card-title>Consulta de Pessoas</v-card-title>
      <v-card-text>
        <v-row align="center">
          <v-col cols="12" md="8">
            <v-text-field
              v-model="searchQuery"
              label="Pesquisar por Nome ou CPF"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              hide-details
              @keyup.enter="handleSearch"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-btn 
              color="primary" 
              size="large" 
              block 
              @click="handleSearch"
              :loading="store.loading"
            >
              Pesquisar
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card>
      <v-data-table
        :headers="headers"
        :items="store.persons"
        :loading="store.loading"
        class="elevation-1"
      >
        <template v-slot:item.sex="{ item }">
          <v-chip :color="item.sex === 'M' ? 'blue' : 'pink'" size="small">
            {{ item.sex === 'M' ? 'Masculino' : 'Feminino' }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn icon="mdi-pencil" size="small" color="warning" class="mr-2"></v-btn>
          <v-btn 
            icon="mdi-delete" 
            size="small" 
            color="error" 
            @click="store.deletePerson(item.id!)"
          ></v-btn>
        </template>
      </v-data-table>
    </v-card>
    
    <v-btn
      position="fixed"
      location="bottom right"
      color="success"
      icon="mdi-plus"
      size="x-large"
      class="mb-4 mr-4"
    ></v-btn>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usePersonStore } from '@/stores/person'

const store = usePersonStore()
const searchQuery = ref('')

const headers = [
  { title: 'Nome', key: 'name' },
  { title: 'CPF', key: 'cpf' },
  { title: 'Nasc.', key: 'date_of_birth' },
  { title: 'Sexo', key: 'sex' },
  { title: 'Peso (kg)', key: 'weight' },
  { title: 'Ideal (kg)', key: 'ideal_weight' },
  { title: 'Ações', key: 'actions', sortable: false },
]

function handleSearch() {
  store.fetchPersons(searchQuery.value)
}

// Carrega dados iniciais
onMounted(() => {
  store.fetchPersons()
})
</script>
