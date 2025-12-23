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
              variant="outlined"
              hide-details
              @keyup.enter="handleSearch"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-btn color="primary" block @click="handleSearch" :loading="store.loading">
              Pesquisar
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card>
      <v-data-table :headers="headers" :items="store.persons" :loading="store.loading">
        <template v-slot:item.sex="{ item }">
          <v-chip :color="item.sex === 'M' ? 'blue' : 'pink'" size="small">
            {{ item.sex === 'M' ? 'Masculino' : 'Feminino' }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn 
            icon="mdi-pencil" 
            size="small" 
            color="warning" 
            class="mr-2"
            @click="openEdit(item)" 
          ></v-btn>
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
      @click="openCreate"
    ></v-btn>

    <PersonForm 
      ref="personFormRef"  v-model="formDialog" 
      :item="selectedPerson" 
      :loading="store.loading"
      @save="handleSave"
    />

  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usePersonStore, type Person } from '@/stores/person'
// Certifique-se de criar este arquivo conforme o passo anterior
import PersonForm from '@/components/PersonForm.vue' 

const store = usePersonStore()
const searchQuery = ref('')

// --- ESTADOS DO FORMULÁRIO ---
const formDialog = ref(false)         // Controla se o modal aparece
const selectedPerson = ref<Person | null>(null) // Armazena os dados para edição

const headers = [
  { title: 'Nome', key: 'name' },
  { title: 'CPF', key: 'cpf' },
  { title: 'Nasc.', key: 'date_of_birth' },
  { title: 'Sexo', key: 'sex' },
  { title: 'Peso (kg)', key: 'weight' },
  { title: 'Ideal (kg)', key: 'ideal_weight' },
  { title: 'Ações', key: 'actions', sortable: false },
]

const personFormRef = ref<any>(null)

// --- MÉTODOS ---

function handleSearch() {
  store.fetchPersons(searchQuery.value)
}

// Abre para criar (limpa o selecionado)
function openCreate() {
  selectedPerson.value = null
  formDialog.value = true
}

// Abre para editar (passa a pessoa da linha da tabela)
function openEdit(person: Person) {
  selectedPerson.value = { ...person } // Usamos spread para não alterar a lista antes de salvar
  formDialog.value = true
}

// Envia para o Pinia salvar
async function handleSave(personData: Person) {
  const result = await store.savePerson(personData)
  
  if (result.success) {
    formDialog.value = false
  } else {
    // Passa os erros do DRF (ex: { cpf: ["CPF inválido"] }) para o formulário
    personFormRef.value?.setErrors(result.errors)
  }
}

onMounted(() => {
  store.fetchPersons()
})
</script>