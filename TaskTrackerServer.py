import grpc
from google.protobuf.timestamp_pb2 import Timestamp
import TaskTracker_pb2
import TaskTracker_pb2_grpc

from concurrent import futures
import logging

class TaskTrackerServicer(TaskTracker_pb2_grpc.TaskTrackerServicer):
    def __init__(self) -> None:
        self.tasks = []

    def CreateTask(self, request, context):
        new_task = TaskTracker_pb2.Task(Title=request.Title, Content=request.Content, Tag=request.Tag)
        new_task.Id = len(self.tasks) + 1
        new_task.Created.GetCurrentTime() # sim, "Get" usado para atribuir valor a si mesmo
        self.tasks.append(new_task)
        return TaskTracker_pb2.CreateTaskResponse(TaskId=new_task.Id)
    
    def ListTask(self, request, context):
        response = TaskTracker_pb2.ListTaskResponse(List=self.tasks)
        return response
    
    def ExecuteTask(self, request, context): 
        task = next((t for t in self.tasks if t.Id == request.TaskId), None)
        if task is None:
            return TaskTracker_pb2.ExecuteTaskResponse(Error=1)  # Tarefa não encontrada
        
        task.Started.GetCurrentTime()
        return TaskTracker_pb2.ExecuteTaskResponse(Error=0)

    def FinalizeTask(self, request, context):
        task = next((t for t in self.tasks if t.Id == request.TaskId), None)
        if task is None:
            return TaskTracker_pb2.FinalizeTaskResponse(Error=1)  # Tarefa não encontrada
        
        task.Ended.GetCurrentTime()
        return TaskTracker_pb2.FinalizeTaskResponse(Error=0)

    def RemoveTask(self, request, context):
        task = next((t for t in self.tasks if t.Id == request.TaskId), None)
        if task is None:
            return TaskTracker_pb2.RemoveTaskResponse(Error=1)  # Tarefa não encontrada
        self.tasks.remove(task)
        return TaskTracker_pb2.RemoveTaskResponse(Error=0)  # Tarefa removida com sucesso

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    TaskTracker_pb2_grpc.add_TaskTrackerServicer_to_server(TaskTrackerServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started at [::]:50051")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
