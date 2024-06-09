class Turn:
    type = "unknown"
    def __init__(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y
    def getType(self):
        return self.type

class MoveTurn(Turn):
    type = "move"
    def __init__(self, target_x, target_y, start_x, start_y):
        super().__init__(start_x, start_y)
        self.target_x = target_x
        self.target_y = target_y
    def __str__(self):
        return f"Move to ({self.target_x}, {self.target_y})"
    def toDict(self):
        return {"type": "move", "target_x": self.target_x, "target_y": self.target_y}

class AttackTurn(Turn):
    type = "attack"
    def __init__(self, monster_idx, start_x, start_y):
        super().__init__(start_x, start_y)
        self.idx = monster_idx
    def __str__(self):
        return f"Attack monster {self.idx}"
    def toDict(self):
        return {"type": "attack", "target_id": self.idx}