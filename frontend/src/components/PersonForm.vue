<template>
  <v-dialog v-model="dialog" max-width="600px" persistent>
    <v-card>
      <v-card-title class="pa-4 bg-primary text-white">
        <span class="text-h5">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="formRef">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field 
                  v-model="editedItem.name" 
                  label="Nome Completo" 
                  :error-messages="serverErrors.name"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field 
                  v-model="editedItem.cpf" 
                  label="CPF" 
                  :error-messages="serverErrors.cpf"
                  placeholder="000.000.000-00"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field 
                  v-model="editedItem.date_of_birth" 
                  label="Data de Nascimento" 
                  type="date"
                  persistent-placeholder
                  :error-messages="serverErrors.date_of_birth"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="4">
                <v-select 
                  v-model="editedItem.sex" 
                  :items="[{t: 'Masc', v: 'M'}, {t: 'Fem', v: 'F'}]" 
                  item-title="t" item-value="v" 
                  label="Sexo"
                  :error-messages="serverErrors.sex"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="4">
                <v-text-field 
                  v-model.number="editedItem.height" 
                  label="Altura (m)" 
                  type="number" step="0.01"
                  :error-messages="serverErrors.height"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="4">
                <v-text-field 
                  v-model.number="editedItem.weight" 
                  label="Peso (kg)" 
                  type="number" step="0.1"
                  :error-messages="serverErrors.weight"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        
        <v-alert v-if="serverErrors.detail" type="error" class="mt-2">
          {{ serverErrors.detail }}
        </v-alert>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey-darken-1" variant="text" @click="close">Cancelar</v-btn>
        <v-btn color="primary" :loading="loading" @click="save">Salvar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = defineProps(['modelValue', 'item', 'loading'])
const emit = defineEmits(['update:modelValue', 'save'])

const serverErrors = ref<any>({}) // Onde guardamos os erros do DRF

const editedItem = ref({
  name: '', cpf: '', date_of_birth: '', sex: 'M', height: 0, weight: 0
})

const dialog = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const formTitle = computed(() => editedItem.value.id ? 'Editar Pessoa' : 'Nova Pessoa')

// Limpa erros ao abrir/fechar
watch(dialog, (val) => {
  if (val) {
    serverErrors.value = {}
    editedItem.value = props.item ? { ...props.item } : { name: '', cpf: '', date_of_birth: '', sex: 'M', height: 1.70, weight: 70 }
  }
})

// Função para o componente pai injetar os erros
function setErrors(errors: any) {
  serverErrors.value = errors
}

defineExpose({ setErrors }) // Permite que o pai chame essa função

function close() {
  dialog.value = false
}

function save() {
  serverErrors.value = {} // Reseta erros antes de tentar salvar
  emit('save', editedItem.value)
}
</script>
