from math import floor

class Hero:
    """
    Hero class, I often work with square distances (for speed and range) so I compute them in advance.
    Also the compute distance function in the utils file only computes the squared distance, to get the 
    real distance one must tak ethe square root of the result.
    """
    def __init__(self, x, y, base_speed, base_power, base_range, level_speed_coeff, level_power_coeff, level_range_coeff):
        self.x = x
        self.y = y
        self.base_speed = base_speed
        self.base_power = base_power
        self.base_range = base_range
        self.level_speed_coeff = level_speed_coeff
        self.level_power_coeff = level_power_coeff
        self.level_range_coeff = level_range_coeff
        self.level = 0
        self.gold = 0
        self.exp = 0
        self.recomputeStats()

    def computeSpeed(self):
        return floor(self.base_speed * (1 + self.level * self.level_speed_coeff / 100))
    def computePower(self):
        return floor(self.base_power * (1 + self.level * self.level_power_coeff / 100))
    def computeRange(self):
        return floor(self.base_range * (1 + self.level * self.level_range_coeff / 100))
    
    def killMonster(self, monster):
        self.getGold(monster.gold)
        self.getExp(monster.exp)
    def undoKillMonster(self, monster):
        self.undoGetGold(monster.gold)
        self.undoGetExp(monster.exp)
    
    def getGold(self, gold):
        self.gold += gold
    def undoGetGold(self, gold):
        self.gold -= gold
    
    def getExp(self, exp):
        self.exp += exp
        while self.exp >= Hero.xpToLevelUp(self.level+1):
            self.levelUp()
    def undoGetExp(self, exp):
        self.exp -= exp
        while self.exp < 0:
            self.undoLevelUp()
    
    def levelUp(self):
        self.level += 1
        self.exp -= Hero.xpToLevelUp(self.level)
        self.recomputeStats()
    def undoLevelUp(self):
        self.exp += Hero.xpToLevelUp(self.level)
        self.level -= 1
        self.recomputeStats()
    
    def move(self, x, y):
        self.x = x
        self.y = y
    def undoMove(self, x, y):
        self.x = x
        self.y = y
    
    def xpToLevelUp(lvl):
        return 1000 + lvl * (lvl - 1) * 50
    
    def recomputeStats(self):
        self.speed = self.computeSpeed()
        self.sqspeed = self.speed**2
        self.power = self.computePower()
        self.range = self.computeRange()
        self.sqrange = self.range**2