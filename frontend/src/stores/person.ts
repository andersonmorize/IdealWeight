import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'

// Interface baseada no seu Backend
export interface Person {
  id?: number
  name: string
  cpf: string
  date_of_birth: string
  sex: 'M' | 'F'
  height: number
  weight: number
  ideal_weight?: number
}

export const usePersonStore = defineStore('person', () => {
  const persons = ref<Person[]>([])
  const loading = ref(false)

  // Configuração base do Axios (ajuste a URL se necessário)
  const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1' 
  })

  async function fetchPersons(search: string = '') {
    loading.value = true
    try {
      // O backend espera ?search=... para filtrar nome ou CPF
      const response = await api.get(`/persons/?search=${search}`)
      persons.value = response.data.results || response.data
    } catch (error) {
      console.error('Erro ao buscar pessoas:', error)
    } finally {
      loading.value = false
    }
  }

  async function deletePerson(id: number) {
    if(!confirm('Tem certeza que deseja excluir?')) return;
    try {
        await api.delete(`/persons/${id}/`);
        // Remove da lista localmente para não precisar recarregar
        persons.value = persons.value.filter(p => p.id !== id);
    } catch (error) {
        alert('Erro ao excluir');
    }
  }

  return { persons, loading, fetchPersons, deletePerson }
})
