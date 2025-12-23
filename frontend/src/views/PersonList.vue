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

    <v-row class="mb-4">
      <v-col cols="12" class="d-flex">
        <v-btn
          color="secondary"
          prepend-icon="mdi-export"
          class="me-3" 
          :loading="store.exportStatus.loading"
          @click="store.startExport"
        >
          Exportar CSV
        </v-btn>

        <v-btn
          color="info"
          prepend-icon="mdi-import"
          disabled
          :loading="store.importStatus.loading"
          @click="$refs.fileInput.click()"
        >
          Importar CSV
        </v-btn>

        <input
          ref="fileInput"
          type="file"
          accept=".csv"
          style="display: none"
          @change="onFileSelected"
        />
      </v-col>
    </v-row>

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
            icon="mdi-scale-balance" 
            size="small" 
            color="info" 
            class="mr-2"
            @click="handleCalculateIdealWeight(item.id!)"
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
  <v-dialog v-model="idealWeightDialog" max-width="400">
    <v-card>
      <v-card-title class="text-h5">Peso Ideal Calculado</v-card-title>
      <v-card-text class="text-center py-4">
        <div class="text-h4 font-weight-bold text-primary">
          {{ calculatedWeight }} kg
        </div>
        <p class="mt-2 text-grey">Resultado baseado na fórmula oficial.</p>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" variant="text" @click="idealWeightDialog = false">Fechar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-dialog v-model="errorModal" max-width="600px">
    <v-card>
      <v-card-title class="bg-error text-white d-flex align-center">
        <v-icon start>mdi-alert-circle</v-icon>
        Erros na Importação
      </v-card-title>
      
      <v-card-text class="pt-4">
        <p class="mb-4">Algumas linhas do CSV não puderam ser processadas:</p>
        
        <v-list density="compact" class="bg-grey-lighten-4 rounded">
          <v-list-item v-for="(error, index) in store.importErrors" :key="index">
            <template v-slot:prepend>
              <v-icon color="error" size="small">mdi-close-circle-outline</v-icon>
            </template>
            <v-list-item-title class="text-wrap text-caption text-red-darken-2">
              {{ error }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey-darken-1" variant="text" @click="errorModal = false">Fechar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usePersonStore, type Person } from '@/stores/person'
import { watch } from 'vue'
import PersonForm from '@/components/PersonForm.vue' 

const store = usePersonStore()
const searchQuery = ref('')

// --- ESTADOS DO FORMULÁRIO ---
const formDialog = ref(false)         // Controla se o modal aparece
const selectedPerson = ref<Person | null>(null) // Armazena os dados para edição

// --- NEW STATE FOR POPUP ---
const idealWeightDialog = ref(false)
const calculatedWeight = ref<number | null>(null)

const headers = [
  { title: 'Nome', key: 'name' },
  { title: 'CPF', key: 'cpf' },
  { title: 'Nasc.', key: 'date_of_birth' },
  { title: 'Sexo', key: 'sex' },
  { title: 'Peso (kg)', key: 'weight' },
  { title: 'Altura (m)', key: 'height' },
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

async function handleCalculateIdealWeight(id: number) {
  const result = await store.getIdealWeight(id)
  if (result.success) {
    calculatedWeight.value = result.weight
    idealWeightDialog.value = true
  } else {
    alert('Erro ao calcular peso ideal: ' + result.error)
  }
}

const fileInput = ref<HTMLInputElement | null>(null)

async function onFileSelected(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    await store.uploadCSV(target.files[0])
    // Limpa o input para permitir selecionar o mesmo arquivo novamente se necessário
    target.value = ''
  }
}

const errorModal = ref(false)

// Observa o store: se surgirem novos erros, abre o modal
watch(() => store.importErrors, (newErrors) => {
  if (newErrors.length > 0) {
    errorModal.value = true
  }
})

onMounted(() => {
  store.fetchPersons()
})
</script>