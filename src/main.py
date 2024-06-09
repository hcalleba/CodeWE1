import os
import json
from Hero import Hero
from Game import Game
from Monster import Monster
from Map import Map

def load_json(n):
    f = open("data/heropath_inputs_day1/" + f"{n:03}" + ".json", "r")
    data = json.load(f)
    return data

def save_json(n, data):
    if not os.path.exists("data/heropath_outputs_day1/"):
        os.makedirs("data/heropath_outputs_day1/")
    f = open("data/heropath_outputs_day1/" + f"{n:03}" + ".json", "w")
    json.dump({"moves": [move.toDict() for move in data]}, f, indent=4)

def extract_data(n):
    data = load_json(n)
    hero = Hero(data["start_x"], data["start_y"], data["hero"]["base_speed"], data["hero"]["base_power"], data["hero"]["base_range"], data["hero"]["level_speed_coeff"], data["hero"]["level_power_coeff"], data["hero"]["level_range_coeff"])
    map = Map(data["width"], data["height"])
    monsters = []
    monster_idx = 0
    for monster in data["monsters"]:
        monsters.append(Monster(monster["x"], monster["y"], monster["hp"], monster["gold"], monster["exp"], monster_idx))
        monster_idx += 1
    return Game(hero, monsters, map, data["num_turns"])

def main(n, nbFutureMoves, nbBestGold, nbBestExp, nbRand):
    assert nbFutureMoves > 0
    game = extract_data(n)
    game.futureMoves = nbFutureMoves
    game.nbBestGold = nbBestGold
    game.nbBestExp = nbBestExp
    game.nbRand = nbRand
    game.playTurns()
    print("Instance " + f"{n:03}: {game.hero.gold}")
    save_json(n, game.moves)

if __name__ == "__main__":
    for i in range(1, 26):
        main(i, nbFutureMoves = 2, nbBestGold = 10, nbBestExp = 0, nbRand = 0)