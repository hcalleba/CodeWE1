class Monster:
    def __init__(self, x, y, hp, gold, exp, idx):
        self.x = x
        self.y = y
        self.hp = hp
        self.gold = gold
        self.exp = exp
        self.idx = idx
        self.alive = True
    def isAlive(self):
        return self.alive
    def die(self):
        self.alive = False
    def undoDie(self):
        self.alive = True
    def __str__(self):
        return f"Monster {self.idx} at ({self.x}, {self.y}) with {self.hp} hp, {self.gold} gold, {self.exp} exp"