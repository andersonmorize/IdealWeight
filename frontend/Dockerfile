FROM node:20-alpine

WORKDIR /app

# Copia apenas os arquivos de definição de pacotes primeiro
COPY package*.json ./

# Instala as dependências (isso cria a node_modules dentro da imagem)
RUN npm install

# Adiciona o diretório de binários do npm ao PATH do sistema
ENV PATH /app/node_modules/.bin:$PATH

# Copia o restante do código
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
