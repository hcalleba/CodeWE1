from utils import *
from math import floor, ceil, sqrt
from Turn import MoveTurn, AttackTurn
from random import randint

class Game:
    """
    Class that represents the game.
    """
    def __init__(self, hero, monsters, map, turns, futureMoves = 1, nbBestGold = 0, nbBestExp = 0, nbRand = 0):
        """
        The following parameters are used for the greedy search heuristic:
        @param futureMoves: number of future moves to consider
            What I consider a Move is choosing a Monster, moving to it and killing it, which is different from the move of the statement which I call a turn
        @param nbBestGold: number of best monsters to consider based on gold
        @param nbBestExp: number of best monsters to consider based on exp
        @param nbRand: number of random monsters to consider
        """
        self.hero = hero
        self.monsters = monsters
        self.map = map
        self.maxTurns = turns
        self.turn = turns
        self.moves = []
        self.futureMoves = futureMoves
        self.nbBestGold = nbBestGold
        self.nbBestExp = nbBestExp
        self.nbRand = nbRand

    def getNextMonsters(self):
        """
        Returns the indices of the best monsters corresponding to the variables of the Game
        nbBestGold, nbBestExp correspond to the indices of the monsters with the highest gold and exp per turn
        nbRand is how many random monsters should be used.
        """
        # If all parameters are set to 0, return all monsters
        if (self.nbBestGold + self.nbBestExp + self.nbRand) == 0:
            return self.monsters
        
        bestMonsters = []
        # Compute the expected gold per turn for each monster
        expectedScores = []
        for monster in self.monsters:
            if monster.isAlive():
                distWoRange = max(0, sqrt(sq_dist(self.hero.x, self.hero.y, monster.x, monster.y)) - self.hero.range)
                moveTurns = max(0, ceil(distWoRange / self.hero.speed))
                attackTurns = ceil(monster.hp / self.hero.power)
                if moveTurns + attackTurns >= self.turn:
                    expectedScores.append(0)
                else:
                    expectedScores.append(monster.gold / (moveTurns + attackTurns))
            else:
                expectedScores.append(-1)
        for _ in range(self.nbBestGold): # I should probably sort the list and then take the first nbBestGold mmonsters rather than applying iterative max
            bestMonsterIdx = getIdxF(expectedScores, max)
            if expectedScores[bestMonsterIdx] < 0:
                break
            bestMonsters.append(bestMonsterIdx)
            expectedScores[bestMonsters[-1]] = -1
        
        # Compute the expected exp per turn for each monster
        expectedScores = []
        for monster in self.monsters:
            if monster.isAlive():
                distWoRange = max(0, sqrt(sq_dist(self.hero.x, self.hero.y, monster.x, monster.y)) - self.hero.range)
                moveTurns = max(0, ceil(distWoRange / self.hero.speed))
                attackTurns = ceil(monster.hp / self.hero.power)
                if moveTurns + attackTurns >= self.turn:
                    expectedScores.append(0)
                else:
                    expectedScores.append(monster.exp / (moveTurns + attackTurns))
            else:
                expectedScores.append(-1)
        for _ in range(self.nbBestExp):
            bestMonsterIdx = getIdxF(expectedScores, max)
            if expectedScores[bestMonsterIdx] <= 0 or bestMonsterIdx in bestMonsters:
                break
            bestMonsters.append(getIdxF(expectedScores, max))
            expectedScores[bestMonsters[-1]] = -1

        # Choose random monsters, if the chosen monster is already in the list I just skip it and do not redraw a new random monster
        for _ in range(self.nbRand):
            bestMonsterIdx = randint(0, len(self.monsters) - 1)
            if expectedScores[bestMonsterIdx] <= 0 or bestMonsterIdx in bestMonsters:
                continue
            bestMonsters.append(bestMonsterIdx)

        return [self.monsters[monster_idx] for monster_idx in bestMonsters]
    
    def inAttackRange(self, monster_idx):
        """
        Returns if the monster is in attack range of the hero
        """
        return sq_dist(self.hero.x, self.hero.y, self.monsters[monster_idx].x, self.monsters[monster_idx].y) <= self.hero.sqrange
    
    def goto(self, monster_idx):
        """
        Move in the direction of the monster until the hero is in attack range
        """
        while not self.inAttackRange(monster_idx) and self.turn > 0:
            x, y = self.nextMoveTowards(monster_idx)
            self.addTurn(MoveTurn(x, y, self.hero.x, self.hero.y))
            self.hero.move(x, y)
    def undoGoto(self):
        while len(self.moves) > 0 and self.moves[-1].getType() == "move":
            self.hero.undoMove(self.moves[-1].start_x, self.moves[-1].start_y)
            self.undoAddTurn()
    
    def attack(self, monster_idx):
        """
        Attacks the monster until it is dead or the hero runs out of turns
        """
        while self.monsters[monster_idx].hp > 0 and self.turn > 0:
            self.addTurn(AttackTurn(monster_idx, self.hero.x, self.hero.y))
            self.monsters[monster_idx].hp -= self.hero.power
            if self.monsters[monster_idx].hp <= 0:
                self.hero.killMonster(self.monsters[monster_idx])
                self.monsters[monster_idx].die()
    def undoAttack(self):
        monster_idx = self.moves[-1].idx
        if not self.monsters[monster_idx].isAlive():
            self.monsters[monster_idx].undoDie()
            self.hero.undoKillMonster(self.monsters[monster_idx])
        while len(self.moves) > 0 and self.moves[-1].getType() == "attack" and self.moves[-1].idx == monster_idx:
            self.monsters[monster_idx].hp += self.hero.power
            self.undoAddTurn()
    
    def nextMoveTowards(self, monster_idx):
        """
        Returns the next closest (x,y) position from the hero to the monster
        It first computes the closest position rounding the x and y near the player
        Then it only tries to increment x or y while keeping the other equal to the previous rounding
        """
        if sq_dist(self.hero.x, self.hero.y, self.monsters[monster_idx].x, self.monsters[monster_idx].y) <= self.hero.sqspeed:
            return self.monsters[monster_idx].x, self.monsters[monster_idx].y

        xstart, ystart = self.hero.x, self.hero.y
        xdest, ydest = self.monsters[monster_idx].x, self.monsters[monster_idx].y
        dist = sqrt(sq_dist(xstart, ystart, xdest, ydest))
        xfrac, yfrac = (xdest - xstart) / dist, (ydest - ystart) / dist
        
        xbest = xstart + floor(xfrac * self.hero.speed) if xfrac > 0 else xstart + ceil(xfrac * self.hero.speed)
        ybest = ystart + floor(yfrac * self.hero.speed) if yfrac > 0 else ystart + ceil(yfrac * self.hero.speed)
        distbest = sq_dist(xbest, ybest, xdest, ydest)
        
        # Round x near player and increment y
        xtemp = xstart + floor(xfrac * self.hero.speed) if xfrac > 0 else xstart + ceil(xfrac * self.hero.speed)
        ytemp = ystart + floor(yfrac * self.hero.speed) if yfrac > 0 else ystart + ceil(yfrac * self.hero.speed)
        while True:
            ytemp += 1 if yfrac > 0 else -1
            disttemp = sq_dist(xtemp, ytemp, xdest, ydest)
            if sq_dist(xstart, ystart, xtemp, ytemp) > self.hero.sqspeed:
                break
            if disttemp < distbest:
                xbest, ybest = xtemp, ytemp
                distbest = disttemp

        # Round y near player and increment x
        xtemp = xstart + floor(xfrac * self.hero.speed) if xfrac > 0 else xstart + ceil(xfrac * self.hero.speed)
        ytemp = ystart + floor(yfrac * self.hero.speed) if yfrac > 0 else ystart + ceil(yfrac * self.hero.speed)
        while True:
            xtemp += 1 if xfrac > 0 else -1
            disttemp = sq_dist(xtemp, ytemp, xdest, ydest)
            if sq_dist(xstart, ystart, xtemp, ytemp) > self.hero.sqspeed:
                break
            if disttemp < distbest:
                xbest, ybest = xtemp, ytemp
                distbest = disttemp
        
        return xbest, ybest
    
    def addTurn(self, move):
        self.moves.append(move)
        self.turn -= 1
    def undoAddTurn(self):
        self.moves.pop()
        self.turn += 1
    
    def undoMove(self):
        """
        Undoes the last move (which corresponds to a monster kill) done by the hero.
        It will first pop all attack moves with the same monster index
        and then the last movement moves done by the hero (until an attack).
        """
        # Remove all attacks to the same monster
        if self.moves[-1].getType() == "attack":
            self.undoAttack()
        # Remove last movement moves
        if len(self.moves) > 0:
            self.undoGoto()

    def killMonster(self, monster_idx):
        """
        Go towards a monster and kill it
        """
        self.goto(monster_idx)
        self.attack(monster_idx)

    def findNextAndAttack(self, nbMoves=1, master=False):
        """
        Chooses the best monster to kill and kills it based on the next nbMoves moves
        The monsters to choose from are based on getNextMonsters() which returns the best
        monsters based on nbBestGold, nbBestExp and nbRand parameters.
        """
        if nbMoves == 0 or self.turn == 0:
            return self.hero.gold / (self.maxTurns - self.turn)
        scores = []
        indices = []
        for monster in self.getNextMonsters():
            if monster.isAlive() :
                self.killMonster(monster.idx)
                scores.append(self.findNextAndAttack(nbMoves - 1))
                indices.append(monster.idx)
                self.undoMove()
            else:
                scores.append(-1)
                indices.append(monster.idx)
        if master:
            self.killMonster(indices[getIdxF(scores, max)])
        else:
            return max(scores)
    
    def playTurns(self):
        """
        Plays the game until the hero runs out of turns
        The method implemented is a greedy heuristic.
        By default it chooses the monster to kill which gives the most gold per turn,
        allowing to llok up to futureMoves moves ahead.

        You can limit the number of monsters to consider each move based on gold, exp and randomness.
        """
        while self.turn > 0:
            self.findNextAndAttack(self.futureMoves, True)
        self.moves = self.moves[:self.maxTurns]
    
    def printMoves(self):
        print("Moves:")
        for move in self.moves:
            print("\t" + str(move))
