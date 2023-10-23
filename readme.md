# TaskTracker

Aluno **Gustavo Moreira de Mello**

RA: **180525**

Professor: **Marcos Jardini**

Matéria: Sistemas **Distribuidos CP406TIN2**

---

O TaskTracker é uma aplicação GRPC simples para rastreamento de tarefas. Ele permite criar, listar, executar, finalizar e remover tarefas.


## 📋 Pré-requisitos

- **Python 3.x**
- **pip**

## 🚀 Configuração do ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/GustavoMMello01/gRPC-Server.git
cd 180525

```

### 2. Configurar um ambiente virtual
É recomendado usar um ambiente virtual para evitar conflitos de pacotes. Você pode usar venv para criar um:
- Windows
```bash
.\venv\Scripts\activate

```

- Linux/Mac
```bash
source venv/bin/activate

```

### 3. Instalar as dependências
Após ativar o ambiente virtual, instale as dependências necessárias:
```bash
pip install -r requirements.txt
    
```


## 🎮 Execução
### 1. Iniciar o servidor GRPC

```bash
python TaskTrackerServer.py
```

### 2. Iniciar o cliente GRPC
Em um novo terminal (necessário ativar o ambiente virtual novamente):
```bash
python TaskTrackerClient.py
```

## Observações
Se necessario atualizar o .proto, realizar o seguinte comando no CMD para windows:
```bash
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=.  TaskTracker.proto
```

