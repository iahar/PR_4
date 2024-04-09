from IMemory import IMemoryManager
from Space import Space
from process import Process
import threading

class ConstantPartitionMemoryManager(IMemoryManager):
    def __init__(self, size, sizeOfSpace, compress):
        self.Mutex = threading.Lock()
        self.Spaces = dict()
        self.totalSize = size
        self.countPages = (int)(size / sizeOfSpace)
        self.fillPages = 0
        self.filSizes = 0
        for i in range(self.countPages):
            space = Space(size)
            self.Spaces[space.id] = space  
    
    def allocate_memory(self, process: Process):
        self.Mutex.acquire()             
        for space in self.Spaces.values():
            if (space.locked == False):
                space.process = process
                space.locked = True
                space.busySize = process.size
                self.fillPages +=1
                self.filSizes += process.size
                process.add_space(space)                 
                break  
        self.Mutex.release()

    def release_memory(self, process: Process):
        self.Mutex.acquire()
        for space in self.Spaces.values():
            if (space.process == process):
                space.locked = False                
                self.fillPages -=1
                self.filSizes -= process.size
                break
        process.clear_space()
        self.Mutex.release()        

    def get_status(self):
        return f"Менеджер памяти с постоянными разделами: Занято разделов: {self.fillPages} Занято памяти: {self.filSizes}"
    
    def wakeup_process(self, process: Process):
        return
