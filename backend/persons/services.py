from celery.result import AsyncResult

from .tasks import PersonTask, import_persons_from_csv, export_persons_to_csv


class PersonService:
    """
    Classe Service: Atua entre o Controller e a Task.
    """
    @staticmethod
    def handle_create(dto_data):
        return PersonTask.create(dto_data)

    @staticmethod
    def handle_update(person_id, dto_data):
        return PersonTask.update(person_id, dto_data)

    @staticmethod
    def handle_delete(person_id):
        return PersonTask.delete(person_id)

    @staticmethod
    def handle_search(filters, search_term):
        return PersonTask.filter_people(filters, search_term)

    @staticmethod
    def get_person_by_id(person_id):
        return PersonTask.get_by_id(person_id)

    @staticmethod
    def get_ideal_weight_calculation(person_id):
        """
        Lógica para o ponto extra solicitada na prova.
        """
        person = PersonTask.get_by_id(person_id)
        height = float(person.height)
        
        # Fórmulas exigidas: Homem: (72.7 * altura) - 58 | Mulher: (62.1 * altura) - 44.7
        if person.sex == 'M':
            ideal_weight = (72.7 * height) - 58
        else:
            ideal_weight = (62.1 * height) - 44.7
            
        return round(ideal_weight, 2)

    @staticmethod
    def handle_import_csv(file):
        """
        Lê o arquivo, extrai o conteúdo e dispara a task assíncrona.
        Retorna o ID da tarefa para rastreamento.
        """
        # 1. Lê o conteúdo do arquivo enviado (em memória)
        try:
            file_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError("O arquivo deve estar no formato UTF-8.")

        # 2. Dispara a task do Celery (usa .delay() para ser assíncrono)
        task = import_persons_from_csv.delay(file_content)
        
        # 3. Retorna o ID da tarefa para o Controller informar ao Client
        return task.id

    @staticmethod
    def get_task_status(task_id):
        """
        Consulta o estado atual da tarefa no Redis.
        """
        task_result = AsyncResult(task_id)
        return {
            "task_id": task_id,
            "status": task_result.status, # PENDING, PROGRESS, SUCCESS, FAILURE
            "result": task_result.result if task_result.ready() else None
        }
    
    @staticmethod
    def handle_export_csv():
        """
        Inicia o processo de exportação assíncrona.
        """
        task = export_persons_to_csv.delay()
        return task.id

    @staticmethod
    def get_export_status(task_id):
        """
        Verifica se o CSV está pronto e retorna o caminho do arquivo.
        """
        task_result = AsyncResult(task_id)
        data = {
            "status": task_result.status,
            "file_url": None
        }
        
        if task_result.ready() and task_result.status == 'SUCCESS':
            file_path = task_result.result.get("file_url")
            data["file_url"] = f"http://localhost:8080/media/{file_path}"
            
        return data