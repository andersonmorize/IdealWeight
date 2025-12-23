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

  const importStatus = ref({ loading: false, progress: 0, error: null as string | null })
  const exportStatus = ref({ loading: false, downloadUrl: null as string | null })
  const importErrors = ref<string[]>([])
  
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

  async function savePerson(person: Person) {
    loading.value = true
    try {
      if (person.id) {
        const response = await api.put(`/persons/${person.id}/`, person)
        const index = persons.value.findIndex(p => p.id === person.id)
        if (index !== -1) persons.value[index] = response.data
      } else {
        const response = await api.post('/persons/', person)
        persons.value.unshift(response.data)
      }
      return { success: true }
    } catch (error: any) {
      return { 
        success: false, 
        errors: error.response?.data || { detail: 'Erro inesperado no servidor' } 
      }
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

  async function getIdealWeight(id: number) {
    try {
      const response = await api.get(`/persons/${id}/calculate_ideal_weight/`)

      return { 
        success: true, 
        weight: response.data.ideal_weight 
      }
    } catch (error: any) {
      console.error('Erro ao calcular:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Erro na requisição' 
      }
    }
  }

  // --- EXPORTAÇÃO ---
  async function startExport() {
    exportStatus.value.loading = true
    try {
      const { data } = await api.post('/persons/export_csv/')
      pollExportStatus(data.task_id)
    } catch (error) {
      exportStatus.value.loading = false
      alert('Erro ao iniciar exportação')
    }
  }

  async function pollExportStatus(taskId: string) {
    try {
      const { data } = await api.get(`/persons/export-status/${taskId}/`)
      if (data.status === 'SUCCESS') {
        exportStatus.value.downloadUrl = data.file_url
        exportStatus.value.loading = false
        // Opcional: Abrir download automaticamente
        window.open(data.file_url, '_blank')
      } else if (data.status === 'FAILURE') {
        throw new Error('Falha no processamento')
      } else {
        // Continua tentando após 2 segundos
        setTimeout(() => pollExportStatus(taskId), 2000)
      }
    } catch (e) {
      exportStatus.value.loading = false
      alert('Erro ao processar arquivo de exportação')
    }
  }

  // --- IMPORTAÇÃO ---
  async function uploadCSV(file: File) {
    importStatus.value.loading = true
    const formData = new FormData()
    formData.append('file', file)

    try {
      const { data } = await api.post('/persons/import_csv/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      pollImportStatus(data.task_id)
    } catch (error: any) {
      importStatus.value.loading = false
      alert(error.response?.data?.error || 'Erro no upload')
    }
  }

  async function pollImportStatus(taskId: string) {
    try {
      const { data } = await api.get(`/persons/import-status/${taskId}/`)
      
      if (data.status === 'SUCCESS') {
        importStatus.value.loading = false
        
        // Se houver erros no objeto result, armazena-os
        if (data.result && data.result.errors && data.result.errors.length > 0) {
          importErrors.value = data.result.errors
        } else {
          importErrors.value = []
          alert('Importação concluída com sucesso!')
        }
        
        fetchPersons() // Atualiza a lista com o que foi importado com sucesso
      } else if (data.status === 'FAILURE') {
        importStatus.value.loading = false
        alert('Erro crítico no servidor durante a importação.')
      } else {
        setTimeout(() => pollImportStatus(taskId), 2000)
      }
    } catch (e) {
      importStatus.value.loading = false
    }
  }

  return { persons, loading, fetchPersons, deletePerson, savePerson, getIdealWeight,
    importStatus, exportStatus, startExport, uploadCSV
   }
})
