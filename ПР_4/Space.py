import uuid

class Space:
    def __init__(self, size):
        self.id = uuid.uuid4()
        self.size = size
        self.locked = False
        self.busySize = 0
        self.type = 0
        self.process = None
        self.position = 0