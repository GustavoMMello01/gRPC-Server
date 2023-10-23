from concurrent import futures
import logging
import grpc
from google.protobuf.timestamp_pb2 import Timestamp
import TaskTracker_pb2
import TaskTracker_pb2_grpc

class TaskTrackerServicer(TaskTracker_pb2_grpc.TaskTrackerServicer):
    # Inicializando o servidor com as listas de tasks e o contador de tasks
    def __init__(self) -> None:
        self.Todo_Tasks = []
        self.Doing_Tasks = []
        self.Done_Tasks = []
        self.TaskCount = 0

    def CreateTask(self, request, context):
        # Criando um novo task com os dados da requisição e adicionando na lista de tasks
        logging.info("Received request to create task with title: {}".format(request.Title))
        newTask = TaskTracker_pb2.Task(Title=request.Title, Content=request.Content, Tag=request.Tag)
        self.TaskCount += 1
        newTask.Id = self.TaskCount
        self.Todo_Tasks.append(newTask)
        # Retornando uma resposta com o ID do novo task criado
        logging.info("Task with title {} created with ID: {}".format(request.Title, newTask.Id))
        # Retorna uma resposta com o ID do novo task criado
        return TaskTracker_pb2.CreateTaskResponse(TaskId=newTask.Id)

    def ListTask(self, request, context):
        # Listando todos os tasks do servidor atraves de uma requisição com filtro
        logging.info("Received request to list tasks.")
        tasks = []
        if request.Filter == TaskTracker_pb2.TQ_TODO: # Filtrando tasks que estão na lista Todo_Tasks
            tasks = self.Todo_Tasks.copy()
        elif request.Filter == TaskTracker_pb2.TQ_DOING: # Filtrando tasks que estão na lista Doing_Tasks
            tasks = self.Doing_Tasks.copy()
        elif request.Filter == TaskTracker_pb2.TQ_DONE: # Filtrando tasks que estão na lista Done_Tasks
            tasks = self.Done_Tasks.copy()
        # Iterando sobre a lista de tasks retornada pelo servidor
        logging.info("Tasks fetched based on the request.")
        return TaskTracker_pb2.ListTaskResponse(List=tasks)

    def ExecuteTask(self, request, context):
        # Executando um task do servidor atraves de uma requisição com o ID do task
        logging.info("Received request to execute task with ID: {}".format(request.TaskId))
        err = 1
        task = next((t for t in self.Todo_Tasks if t.Id == request.TaskId), None)
        if task: # Verificando se o task existe
            self.Todo_Tasks.remove(task)
            task.Started.GetCurrentTime()
            self.Doing_Tasks.append(task)
            err = 0
        logging.info("Task with ID {} executed.".format(request.TaskId))
        return TaskTracker_pb2.ExecuteTaskResponse(Error=err)

    def FinalizeTask(self, request, context):
        # Finalizando um task do servidor atraves de uma requisição com o ID do task
        logging.info("Received request to finalize task with ID: {}".format(request.TaskId))
        err = 1
        task = next((t for t in self.Doing_Tasks if t.Id == request.TaskId), None) # Verificando se o task existe na lista Doing_Tasks
        if task: 
            self.Doing_Tasks.remove(task)
            task.Ended.GetCurrentTime()
            self.Done_Tasks.append(task)
            err = 0
        logging.info("Task with ID {} finalized.".format(request.TaskId))
        return TaskTracker_pb2.FinalizeTaskResponse(Error=err)

    def RemoveTask(self, request, context): 
        # Removendo um task do servidor atraves de uma requisição com o ID do task
        logging.info("Received request to remove task with ID: {}".format(request.TaskId))
        err = 1
        task = next((t for t in self.Todo_Tasks if t.Id == request.TaskId), None)
        if task: # Verificando se o task existe na lista Todo_Tasks
            self.Todo_Tasks.remove(task)
            err = 0
        logging.info("Task with ID {} removed.".format(request.TaskId))
        return TaskTracker_pb2.RemoveTaskResponse(Error=err)

def serve(): 
    # Iniciando o servidor e criando um canal de comunicação com o cliente
    logging.warning("Iniciando Servidor...")
    # Criando um servidor com 2 workers para processar as requisições
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    # Adicionando o servicer ao servidor
    TaskTracker_pb2_grpc.add_TaskTrackerServicer_to_server(TaskTrackerServicer(), server)
    # Iniciando o servidor na porta 50051
    server.add_insecure_port("[::]:50051")
    server.start()
    logging.warning("Servidor Iniciado")
    server.wait_for_termination()

if __name__ == "__main__":
    # Iniciando o servidor e chamando a função serve()
    logging.basicConfig(level=logging.INFO)
    serve()