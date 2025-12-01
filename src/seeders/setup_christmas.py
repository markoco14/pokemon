import sqlite3


vocabulary = [
        ( 
            "Snowball",
            "https://ik.imgkit.net/3vlqs5axxjf/TW-Asia/uploadedImages/Columns/By_the_Way/snowball-in-japan.jpg?width=168&height=168&mode=crop&Anchor=MiddleCenter&tr=w-1200%2Cfo-auto" ,
            "A hand holding a snowball.",
        ),
        ( 
            "Snowman",
            "https://www.bobvila.com/wp-content/uploads/2022/12/iStock-1311241691-how-to-build-a-snowman-decorated-snowman.jpg?quality=85&w=1200" ,
            "A snowman on a hill.",
        ),
        ( 
            "Sleigh",
            "https://api-assets.portablenorthpole.com/prod/santasVillage_fact/5c09/59af7e1b6/897789783efc16b22f992cc8258d3e37.jpeg" ,
            "Santa's sleigh.",
            
        ),
        ( 
            "Reindeer",
            "https://static.vecteezy.com/system/resources/thumbnails/068/910/006/small/snowy-reindeer-herd-winter-landscape-photo.jpg" ,
            "Santa's reindeer.",
        ),
        ( 
            "Rudolph",
            "https://ew.com/thmb/Y56hjhBVvWth0IPh4-1EPxKgJas=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Rudolph_178-e0ee390bba104cd78a01278e5706c798.jpg" ,
            "Rudolph the red-nosed reindeer.",
        ),
        ( 
            "Santa",
            "https://thumbs.dreamstime.com/b/cartoon-santa-claus-snowy-landscape-general-381013987.jpg" ,
            "Santa looking cool.",
        ),
        ( 
            "Elves",
            "https://www.shutterstock.com/image-vector/set-elf-cartoon-character-illustration-600nw-2272423401.jpg" ,
            "Santa's elves looking cool.",
        ),
        ( 
            "Gifts",
            "https://s3.ap-south-1.amazonaws.com/assets.klayschools.com/wp-content/uploads/2024/11/29083250/47-scaled.webp" ,
            "Gifts under the tree.",
            
        ),
        ( 
            "Christmas lights",
            "https://m.media-amazon.com/images/I/71T9EwoNDsL._AC_UF894,1000_QL80_.jpg" ,
            "Christmas lights.",
        ),
        ( 
            "Christmas tree",
            "https://cdn.shopify.com/s/files/1/0778/2679/files/christmas_tree_image_1024x1024.jpg?16688787952827883668" ,
            "A beautiful Christmas tree.",
        ),
        ( 
            "Candy canes",
            "https://media.istockphoto.com/id/183058419/photo/christmas-peppermint-candy-canes-holiday-sweet-food-dessert-background.jpg?s=612x612&w=0&k=20&c=R5_Hun6e9nQgz038ar5PNKsASiD7avbMe2xvUoNGKVk=" ,
            "A pile of candy canes.",
        ),
        ( 
            "Milk and cookies",
            "https://cdn.shopify.com/s/files/1/1016/2961/articles/Santa_Milk_Cookies_Christmas_Eve_ea868994-7a2c-4c1a-9c64-a8bae86b30bf.jpg?v=1679346863" ,
            "Santa's milk and cookies.",
        ),
]

def setup_christmas():
    print("setting up christmas db")
    with sqlite3.connect("esl.db") as conn:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        insert_query = "INSERT INTO christmas (name, large_img_path, alt_text) VALUES (?, ?, ?);"
        cursor.executemany(insert_query, vocabulary)

        conn.commit()
    print("set up complete")