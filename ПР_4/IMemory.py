from process import Process

class IMemoryManager():
    def __init__(self, size, sizeOfSpace, compress): 
        pass
    def allocate_memory(self, process: Process):
        pass
    def release_memory(self, process: Process):
        pass
    def wakeup_process(self, process: Process):
        pass
    def get_status(self):
        pass

    

#void Init(int size);
#void Init(int size, int sizeOfSpace);
#void AddTask(Task task, CancellationToken token);
#void ClearTask(Task task);
#void UnloadMemorySpace(Guid id);
#void LoadMemorySpace(Guid id, CancellationToken token);
#void GetStatus(StatusModel status);