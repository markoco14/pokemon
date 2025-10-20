from src.models.monster import Monster


monsters = ["vampire", "zombie", "mummy", "werewolf", "witch", "ghost", "skeleton", "jack-o-lantern", "scarecrow"]

for monster in monsters:
    Monster.create(name=monster)

db_monsters = Monster.list()

for monster in db_monsters:
    print(monster)