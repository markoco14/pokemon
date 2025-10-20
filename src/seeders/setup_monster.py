from src.models.monster import Monster

monsters = [
    ("vampire", "https://static.vecteezy.com/system/resources/previews/060/849/941/non_2x/cute-vampire-cartoon-character-thumbs-up-free-vector.jpg"),
    ("zombie", "https://img.freepik.com/premium-vector/cute-zombie-from-grave-cartoon-illustration-halloween-concept-isolated_725118-65.jpg"),
    ("mummy", "https://img.freepik.com/premium-photo/cute-mummy-dabbing-cute-cartoon-mummy-doing-dabbing-dance-halloween_924727-39107.jpg"),
    ("werewolf", "https://static.vecteezy.com/system/resources/previews/028/023/480/non_2x/cartoon-angry-werewolf-character-on-white-background-vector.jpg"),
    ("witch", "https://iheartcraftythings.com/wp-content/uploads/2022/02/CartoonWitch-Preview.jpg"),
    ("ghost", "https://heyclipart.com/cdn/shop/files/4-cute-sheet-ghost-vector-cartoon-illustration-30.jpg"),
    ("skeleton", "https://img.freepik.com/free-vector/hand-drawn-skeleton-cartoon-illustration_52683-121182.jpg"),
    ("jack-o-lantern", "https://static.vecteezy.com/system/resources/previews/043/510/512/non_2x/cute-friendly-cartoon-jack-o-lantern-smiling-carved-pumpkin-character-illustration-isolated-on-white-backdrop-concept-of-halloween-kid-friendly-decor-festive-spirit-and-joyful-celebration-vector.jpg"),
    ("scarecrow", "https://www.shutterstock.com/image-vector/scarecrow-rustic-traditional-design-flat-600nw-2503297533.jpg")
    ]

for monster in monsters:
    Monster.create(name=monster[0], large_img_path=monster[1])

db_monsters = Monster.list()

for monster in db_monsters:
    print(monster)