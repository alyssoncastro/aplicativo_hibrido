# Aplicativo de Processamento de Imagens com Flutter e Backend em Microsserviços

###### ALYSSON C. C. CORDEIRO - ENGENHARIA DA COMPUTAÇÃO (INTELI)

## Visão Geral

Este projeto consiste em um aplicativo híbrido desenvolvido em Flutter que permite aos usuários fazer upload de imagens, processá-las (aplicando um filtro preto e branco) e visualizar o resultado. O backend foi desenvolvido utilizando arquitetura de microsserviços, e a aplicação está totalmente conteinerizada utilizando Docker.

## Estrutura do Projeto

A estrutura do projeto é a seguinte:

```python
backend/
├── user_service/
│ ├── app.py
│ ├── database.py
│ ├── Dockerfile
│ ├── models.py
│ ├── requirements.txt
│ ├── docker-compose.yml
├── log_service/
│ ├── app.py
│ ├── database.py
│ ├── Dockerfile
│ ├── models.py
│ ├── requirements.txt
│ ├── docker-compose.yml
├── image_service/
│ ├── app.py
│ ├── Dockerfile
│ ├── requirements.txt
│ ├── docker-compose.yml
├── notification_service/
│ ├── app.py
│ ├── Dockerfile
│ ├── requirements.txt
│ ├── docker-compose.yml
├── docker-compose.yml
└── init.sql
flutter_application_1/
├── lib/
│ ├── main.dart
│ ├── segunda_tela.dart
│ ├── terceira_tela.dart
├── assets/
├── build/
├── pubspec.yaml
├── Dockerfile
└── docker-compose.yml
```


## Funcionalidades

### Frontend (Flutter)
- **Registro de Usuário**: Tela para registrar novos usuários.
- **Login**: Tela para autenticação dos usuários.
- **Upload de Imagens**: Tela para selecionar e fazer upload de imagens.
- **Processamento de Imagens**: A imagem é processada aplicando um filtro preto e branco.
- **Exibição de Imagens Processadas**: Exibe a imagem processada na tela do aplicativo.

### Backend (Microsserviços)
- **user_service**: Gerenciamento de usuários (registro e login).
- **log_service**: Registro de logs das ações dos usuários.
- **image_service**: Recebe e processa imagens (aplicação de filtro preto e branco).
- **notification_service**: Envia notificações após o processamento das imagens.

## Configuração e Execução

### Pré-requisitos
- Docker e Docker Compose
- Flutter SDK

### Instruções de Configuração

1. Clone o repositório:
    ```bash
    git clone https://github.com/alyssoncastro/aplicativo_hibrido.git
    cd aplicativo_hibrido
    ```

2. Navegue até o diretório do backend e inicie os serviços Docker:
    ```bash
    cd backend
    docker-compose up --build
    ```

3. Navegue até o diretório do frontend e inicie o aplicativo Flutter:
    ```bash
    cd flutter_application_1
    flutter run -d chrome
    ```

### Endpoints da API

#### user_service
- `POST /register`: Registra um novo usuário.
- `POST /login`: Autentica um usuário.

#### log_service
- `POST /log`: Cria um novo log.
- `GET /log`: Recupera todos os logs.

#### image_service
- `POST /upload`: Faz o upload e processa uma imagem.
- `GET /uploads/<filename>`: Recupera uma imagem processada.

#### notification_service
- `POST /notify`: Envia uma notificação.

## Exemplo de Uso

1. **Registro e Login**: Registre-se e faça login no aplicativo.
2. **Upload de Imagem**: Selecione uma imagem da galeria e faça o upload.
3. **Processamento e Exibição**: A imagem será processada e o resultado será exibido na tela.

## Tecnologias Utilizadas

- **Frontend**: Flutter
- **Backend**: Python (Flask)
- **Banco de Dados**: PostgreSQL
- **Conteinerização**: Docker, Docker Compose


## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Vídeo da aplicação:

https://drive.google.com/file/d/1JmyFxWLJQde_eXZRsqwjPzYkXF4AC00c/view?usp=sharing

##### Desenvolvido por Alysson C. C. Cordeiro
