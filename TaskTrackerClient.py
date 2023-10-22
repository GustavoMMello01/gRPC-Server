import grpc
from google.protobuf.timestamp_pb2 import Timestamp
import TaskTracker_pb2
import TaskTracker_pb2_grpc
import logging

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = TaskTracker_pb2_grpc.TaskTrackerStub(channel)
        
        print("===== CreateTask =====")
        request1 = TaskTracker_pb2.CreateTaskRequest(Title="Task1", Content="Task 1 is first task", Tag=TaskTracker_pb2.TP_COMMON)
        print("Creating Task: Task1,Task 1 is first task, common", stub.CreateTask(request1))
        
        request2 = TaskTracker_pb2.CreateTaskRequest(Title="Task2", Content="Task 2 is second task", Tag=TaskTracker_pb2.TP_URGENT)
        print("Creating Task: Task2,Task 2 is second task, urgent", stub.CreateTask(request2))
        
        request3 = TaskTracker_pb2.CreateTaskRequest(Title="Task3", Content="Task 3 is third task", Tag=TaskTracker_pb2.TP_PRIORITY)
        print("Creating Task: Task3,Task 3 is third task, priority", stub.CreateTask(request3))
        
        print("\n===== RemoveTask =====")
        removeTaskRequest = TaskTracker_pb2.RemoveTaskRequest(TaskId=2)
        print("Removing Task 2:", stub.RemoveTask(removeTaskRequest))

        print("\n===== ExecuteTask =====")
        executeTaskRequest1 = TaskTracker_pb2.ExecuteTaskRequest(TaskId=1)
        print("Executing Task 1:", stub.ExecuteTask(executeTaskRequest1))
        
        print("\n===== FinalizeTask =====")
        finalizeTaskRequest1 = TaskTracker_pb2.FinalizeTaskRequest(TaskId=1)
        print("Finalizing Task 1:", stub.FinalizeTask(finalizeTaskRequest1))
        
        print("\n===== ListTask =====")
        listTaskRequest = TaskTracker_pb2.ListTaskRequest(Q=TaskTracker_pb2.TQ_TODO, Filter=TaskTracker_pb2.TF_ALL)
        response = stub.ListTask(listTaskRequest)
        for t in response.List:
            created:Timestamp = t.Created
            print(f"Id: {t.Id}")
            print(f"Title: {t.Title}")
            print(f"Content: {t.Content}")
            print(f"Tag: {t.Tag}")
            print(f"Created: {created.ToDatetime():%Y-%m-%d %H:%M:%S}")
            print("-------------------------")

if __name__ == "__main__":
        logging.basicConfig()
        run()
