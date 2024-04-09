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

    # нужно чтоб допустим менялась ячейка на 8 с занятыми 2 с пустой ячейкой на 2
    def compress_memory(self): 
        self.display_memory()
        for i in range(len(self.Spaces)//2):
            if self.Spaces[i].locked == False:
                for j in range(len(self.Spaces)-1, len(self.Spaces)//2, -1):
                    if self.Spaces[j].locked == True:
                        if self.Spaces[j].busySize <= self.Spaces[i].size:
                            temp_i = self.Spaces[i].size
                            temp_j = self.Spaces[j].size
                            self.Spaces[i] = self.Spaces[j]
                            self.Spaces[i].size = temp_i
                            self.Spaces[j] = Space(temp_j)
                            break
        print("-----compress-------")
        self.display_memory()
        
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
        if self.compress: self.compress_memory()
        return f"Менеджер памяти с перемещаемыми разделами: Занято разделов: {self.fillPages}/{self.countPages} Занято памяти: {self.fillSizes}/{self.totalSize}"
    
    def wakeup_process(self, process: Process):
        return

    def display_memory(self): 
        print("Memory Spaces:") 
        for space in self.Spaces: 
            print(f"Size: {space.size}, {'Busy' if space.locked else 'Free'}: {space.busySize}, Process: {space.process.id if space.process else 'None'}")
