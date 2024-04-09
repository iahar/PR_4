from IMemory import IMemoryManager
from Space import Space
from process import Process
import threading

class VariablePartitionMemoryMamager(IMemoryManager):
    def __init__(self, size, sizeOfSpace, compress):
        self.Mutex = threading.Lock()
        self.Spaces = list()
        self.totalSize = size
        self.countPages = 0
        self.fillPages = 0
        self.fillSizes = 0
        self.compress = compress
        cells = [2,4,6,8]
        countSize = 0
        while countSize < size:
            for i in range(4):
                sizeOfSpace = cells[i]
                if ((countSize + sizeOfSpace) <= size):
                    space = Space(sizeOfSpace)
                    self.Spaces.append(space)
                    self.countPages += 1
                    countSize += sizeOfSpace
        self.Spaces.sort(key = lambda item: item.size)

    def compress_memory(self): 
        for i in range(len(self.Space)-1, -1, -1):
            if self.Space[i].locked == False:
                for j in range(i-1, -1, -1):
                    if self.Space[j].locked == True:
                        temp = self.Space[i]
                        self.Space[i] = self.Space[j]
                        self.Space[j] = temp
        
    def allocate_memory(self, process: Process): 
        self.Mutex.acquire()          
        distributed_size = process.size
        if (self.totalSize - self.fillSizes) >= process.size:
            for space in self.Spaces: 
                if space.locked == False:
                    space.type = 1
                    space.process = process
                    space.locked = True                     
                    self.fillPages += 1
                    if space.size >= distributed_size: 
                        self.fillSizes += distributed_size
                        space.busySize += distributed_size
                        distributed_size = 0                        
                    else:
                        self.fillSizes += space.size
                        space.busySize += space.size
                        distributed_size -= space.size                        
                    process.add_space(space)                    
                    if distributed_size == 0:
                        process.countSpace = process.size
                        break  
        else:
            self.compress_memory()              
        self.Mutex.release()

    def release_memory(self, process: Process):
        self.Mutex.acquire()
        for space in process.Spaces:
            if space.process == process:
                space.process = None
                space.locked = False
                space.type = 0
                self.fillPages -= 1
                self.fillSizes -= space.busySize
                space.busySize = 0
        process.clear_space()
        self.Mutex.release()        

    def get_status(self):
        return f"Менеджер памяти с перемещаемыми разделами: Занято разделов: {self.fillPages}/{self.countPages} Занято памяти: {self.fillSizes}/{self.totalSize}"
    
    def wakeup_process(self, process: Process):
        return
