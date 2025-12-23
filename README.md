# IdealWeight
Prova de Recrutamento - Sistema de Gestão de Pessoas e Cálculo de Peso Ideal

Este projeto foi desenvolvido como parte do processo seletivo para a vaga de **Desenvolvedor Fullstack Python**, atendendo a todos os requisitos técnicos e funcionais especificados na prova. A aplicação implementa uma solução completa, moderna e escalável para o cadastro de pessoas, com funcionalidades de CRUD, validações avançadas, cálculo de peso ideal e importação/exportação de dados.

---

## 🎯 **Objetivos Atendidos**

A prova solicitava a criação de uma aplicação web completa para gerenciamento da entidade **Pessoa**, com os seguintes requisitos:

- ✅ **Backend em Django** com arquitetura em camadas (Controller → Service → Task)
- ✅ **API REST** com serialização JSON e validações robustas
- ✅ **Frontend em Vue.js + TypeScript** com interface responsiva e intuitiva
- ✅ **Banco de dados PostgreSQL** com ORM Django
- ✅ **Operações CRUD** completas (Incluir, Alterar, Excluir, Pesquisar)
- ✅ **Cálculo do peso ideal** (ponto extra) com fórmulas distintas para homens e mulheres
- ✅ **Importação/exportação CSV** com processamento assíncrono via Celery + Redis
- ✅ **Testes unitários** abrangentes para modelos, serviços e endpoints
- ✅ **Dockerização completa** com serviços isolados e configuração de rede
- ✅ **Cache com Redis** para otimização de performance
- ✅ **Documentação automática da API** com DRF Spectacular (OpenAPI)

---

## 🏗️ **Arquitetura e Padrões**

### **Backend (Django)**
- **Controller:** `PersonViewSet` (ViewSet do DRF) – gerencia requisições HTTP
- **Service:** `PersonService` – camada de lógica de negócio e orquestração
- **Task:** `PersonTask` – interação direta com o ORM e operações de persistência
- **Model:** `Person` – entidade principal com validações customizadas (CPF, altura, peso)
- **Serializer:** `PersonSerializer` – validação e transformação de dados

### **Frontend (Vue.js 3 + TypeScript)**
- **Pinia** para gerenciamento de estado centralizado
- **Vuetify** para componentes UI modernos e responsivos
- **Axios** para comunicação com a API
- **Arquitetura modular** com stores, views e componentes reutilizáveis

### **Infraestrutura**
- **Docker Compose** para orquestração de serviços
- **PostgreSQL** – banco de dados relacional
- **Redis** – cache e broker para tarefas assíncronas
- **Celery** – processamento de filas (importação/exportação)
- **Nginx** – gateway reverso e servidor de arquivos estáticos

---

## 🚀 **Funcionalidades Implementadas**

### 1. **Cadastro e Gestão de Pessoas**
- Formulário com validação em tempo real
- Campos: Nome, Data de Nascimento, CPF (validado), Sexo, Altura e Peso
- Operações completas: Criar, Listar, Editar, Excluir, Pesquisar (por nome ou CPF)

### 2. **Cálculo do Peso Ideal (Ponto Extra)**
- Fórmula específica por sexo:
  - **Homens:** `(72.7 × altura) - 58`
  - **Mulheres:** `(62.1 × altura) - 44.7`
- Botão dedicado na interface que aciona o cálculo no servidor e exibe resultado em popup

### 3. **Importação/Exportação CSV**
- **Upload de CSV** para cadastro em massa, com processamento assíncrono
- **Exportação para CSV** com link de download automático
- Tratamento de erros por linha e feedback visual para o usuário

### 4. **Validações Avançadas**
- CPF válido (formato e dígitos verificadores)
- Altura e peso dentro de intervalos realistas
- Datas consistentes
- Uniquidade de CPF no banco

### 5. **Performance e Escalabilidade**
- Cache com Redis para consultas frequentes
- Tarefas pesadas (CSV) executadas em background com Celery
- Paginação de resultados na API
- Conexões otimizadas entre serviços Docker

---

## 🛠️ **Tecnologias Utilizadas**

| Camada           | Tecnologias                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **Backend**      | Django, Django REST Framework, Celery, PostgreSQL, Redis, DRF Spectacular   |
| **Frontend**     | Vue.js 3, TypeScript, Pinia, Vuetify, Axios                                |
| **Infra**        | Docker, Docker Compose, Nginx                                              |
| **Testes**       | Django Test Framework, Faker                                               |
| **Validações**   | Validadores customizados (CPF), restrições de modelo, serializers DRF      |

---

## 📁 **Estrutura do Projeto**

```
projeto/
├── backend/                 # Aplicação Django
│   ├── config/             # Settings, URLs, WSGI
│   ├── persons/            # App principal (modelos, views, serviços, tarefas)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Aplicação Vue.js
│   ├── src/
│   │   ├── stores/        # Pinia store (persons.ts)
│   │   ├── views/         # Páginas (PersonList.vue)
│   │   └── components/    # Componentes reutilizáveis
│   └── Dockerfile
├── nginx/                  # Configuração do gateway
├── docker-compose.yml      # Orquestração de serviços
└── README.md               # Este arquivo
```

---

## 🔧 **Como Executar o Projeto**

### 1. **Pré-requisitos**
- Docker e Docker Compose instalados
- Variáveis de ambiente configuradas (`.env`)

### 2. **Subir os serviços**
```bash
docker-compose up --build
```

### 3. **Acessar a aplicação**
- **Frontend:** http://localhost:8080
- **Backend (API):** http://localhost:8000
- **Documentação da API:** http://localhost:8000/api/docs
- **Admin Django:** http://localhost:8000/admin

### 4. **Executar testes**
```bash
docker-compose exec backend python manage.py test
```

### 5. **Geração de Dados de Teste**

O projeto inclui um comando customizado do Django para popular o banco com dados fictícios, útil para desenvolvimento e testes:

```bash
docker-compose exec backend python manage.py generate_persons --number 50
```

**Funcionalidades do comando:**
- Gera nomes masculinos/femininos em português com Faker
- CPFs válidos e formatados
- Datas de nascimento aleatórias (entre 10 e 90 anos)
- Alturas entre 1.50m e 2.00m
- Pesos entre 50kg e 110kg
- Sexo atribuído aleatoriamente (M/F)

---

## ✅ **Diferenciais Técnicos**

1. **Arquitetura limpa e desacoplada** – separação clara entre Controller, Service e Task
2. **TypeScript no frontend** – maior segurança e produtividade no desenvolvimento
3. **Processamento assíncrono** – tarefas de longa duração não bloqueiam a interface
4. **Validação de CPF real** – além do formato, verificação matemática dos dígitos
5. **Cache inteligente** – Redis para otimizar consultas frequentes
6. **Gateway unificado** – Nginx servindo frontend, backend e arquivos estáticos
7. **Testes abrangentes** – cobertura de modelos, serviços, serializers e endpoints
8. **UI profissional** – com Vuetify, seguindo padrões modernos de UX

---

## 🧠 **Decisões de Projeto**

- **Vue.js em vez de Angular:** optei por Vue 3 + TypeScript por sua curva de aprendizado mais suave, performance superior com Composition API e melhor integração com ecossistema moderno.
- **Celery + Redis:** para garantir que operações de CSV não impactem a responsividade da aplicação.
- **Pinia para gerenciamento de estado:** solução oficial e mais simples que Vuex, com melhor suporte a TypeScript.
- **DRF Spectacular:** geração automática de documentação OpenAPI, facilitando integração e testes.
- **Dockerização completa:** ambiente reproduzível, isolado e pronto para produção.

---

## ✨ **Próximas Melhorias (Roadmap)**

- Autenticação e autorização (JWT)
- Dashboard com gráficos de IMC
- Notificações em tempo real (WebSockets)
- Deploy automatizado (CI/CD)
- Logs centralizados (ELK Stack)
- Testes E2E com Cypress

