from IMemory import IMemoryManager
from Space import Space
from process import Process
import threading

class VariablePartitionMemoryMamager(IMemoryManager):
    def __init__(self, size, sizeOfSpace, compress):
        self.Mutex = threading.Lock()
        self.Spaces = [Space(size)]
        self.totalSize = size
        self.countPages = 1
        self.fillSizes = 0
        self.compress = compress
        
    def compress_memory(self): 
        self.display_memory()
        i = 0
        for space1 in self.Spaces:            
            if space1.locked == False:
                j = i+1
                for space2 in self.Spaces[i+1:]:
                    if space2.locked == True:
                        temp = self.Spaces[i]
                        self.Spaces[i] = self.Spaces[j]
                        self.Spaces[j] = temp
                        break
                    else:
                        temp = self.Spaces.pop(j)
                        self.Spaces[i].size += temp.size
                        j -= 1
                        self.countPages -= 1
                        break
                j += 1
            i += 1
        print("-----compress-------")
        self.display_memory()
        
    # алгоритм добавления раздела доделать
    def allocate_memory(self, process: Process): 
        self.Mutex.acquire()  
        temp_size = 0
        for space in self.Spaces:              
            if space.locked == False and space.size >= process.size:
                space.size = process.size
                space.locked = True
                space.process = process
                process.add_space(space)
                process.status = 1                
                self.fillSizes += process.size
                if self.fillSizes < self.totalSize: 
                    self.countPages += 1
                    self.Spaces.append(Space(self.totalSize - temp_size - process.size))
                break
            temp_size += space.size
        self.Mutex.release()

    def release_memory(self, process: Process):
        self.Mutex.acquire()
        for space in self.Spaces:
            if space.process == process:
                space.process = None
                space.locked = False
                space.type = 0
                self.fillSizes -= process.size
                space.busySize = 0
        process.clear_space()
        if self.compress: self.compress_memory()
        self.Mutex.release()        

    def get_status(self):
        return f"Менеджер памяти с перемещаемыми разделами: Разделов: {self.countPages} Занято памяти: {self.fillSizes}/{self.totalSize}"
    
    def wakeup_process(self, process: Process):
        return

    def display_memory(self): 
        print("Memory Spaces:") 
        for space in self.Spaces: 
            print(f"Size: {space.size}, {'Busy' if space.locked else 'Free'}, Process: {space.process.id if space.process else 'None'}")
