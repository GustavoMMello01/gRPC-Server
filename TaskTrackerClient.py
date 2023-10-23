import grpc
import TaskTracker_pb2
import TaskTracker_pb2_grpc
import logging

def run():
    # Criando um canal de comunicação com o servidor
    with grpc.insecure_channel("localhost:50051") as channel:

        # Criando um stub para o canal de comunicação
        stub = TaskTracker_pb2_grpc.TaskTrackerStub(channel)
        
        print("===== CreateTask =====")
        # Criando uma requisição para o servidor com os dados do novo task 
        request1 = TaskTracker_pb2.CreateTaskRequest(Title="Task1", Content="Task 1 is first task", Tag=TaskTracker_pb2.TP_COMMON)
        print("Creating Task:", stub.CreateTask(request1))
        
        request2 = TaskTracker_pb2.CreateTaskRequest(Title="Task2", Content="Task 2 is second task", Tag=TaskTracker_pb2.TP_URGENT)
        print("Creating Task:", stub.CreateTask(request2))
        
        request3 = TaskTracker_pb2.CreateTaskRequest(Title="Task3", Content="Task 3 is third task", Tag=TaskTracker_pb2.TP_PRIORITY)
        print("Creating Task:", stub.CreateTask(request3))
        
        print("\n===== RemoveTask =====")
        # Removendo um task do servidor
        removeTaskRequest = TaskTracker_pb2.RemoveTaskRequest(TaskId=2)
        print("Removing Task 2:", stub.RemoveTask(removeTaskRequest))

        print("\n===== ExecuteTask =====")
        # Executando um task do servidor
        executeTaskRequest1 = TaskTracker_pb2.ExecuteTaskRequest(TaskId=1)
        print("Executing Task 1:", stub.ExecuteTask(executeTaskRequest1))
        
        print("\n===== FinalizeTask =====")
        # Finalizando um task do servidor
        finalizeTaskRequest1 = TaskTracker_pb2.FinalizeTaskRequest(TaskId=1)
        print("Finalizing Task 1:", stub.FinalizeTask(finalizeTaskRequest1))
        
        print("\n===== ListTask =====")
        # Listando todos os tasks do servidor atraves de uma requisição com filtro 
        listTaskRequest = TaskTracker_pb2.ListTaskRequest(Q=TaskTracker_pb2.TQ_TODO, Filter=TaskTracker_pb2.TF_ALL)
        response = stub.ListTask(listTaskRequest)
        # Iterando sobre a lista de tasks retornada pelo servidor
        for t in response.List:
            print(f"Id: {t.Id}")
            print(f"Title: {t.Title}")
            print(f"Content: {t.Content}")
            print(f"Tag: {t.Tag}")
            print("-------------------------")

if __name__ == "__main__":
    # Iniciando o cliente e chamando a função run()
    logging.basicConfig()
    run()
