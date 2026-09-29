import json
import os

letters_data = {
    "A": {"words": ["Apple", "Ant", "Alligator", "Acorn", "Arrow", "Airplane", "Astronaut", "Anchor", "Axe", "Apricot", "Alpaca", "Angel", "Avocado", "Accordion", "Ambulance"], "sound": "/a/"},
    "B": {"words": ["Bear", "Ball", "Butterfly", "Boat", "Book", "Bell", "Bus", "Banana", "Bee", "Bird", "Balloon", "Bat", "Bed", "Button", "Barn"], "sound": "/b/"},
    "C": {"words": ["Cat", "Car", "Cake", "Cow", "Camel", "Castle", "Cloud", "Crown", "Cup", "Clock", "Candy", "Caterpillar", "Camera", "Carrot", "Crab"], "sound": "/k/"},
    "D": {"words": ["Dog", "Duck", "Dinosaur", "Drum", "Doll", "Door", "Desk", "Diamond", "Dice", "Dolphin", "Donut", "Doctor", "Deer", "Dragon", "Dress"], "sound": "/d/"},
    "E": {"words": ["Elephant", "Egg", "Eagle", "Ear", "Eye", "Engine", "Earth", "Eel", "Elbow", "Envelope", "Elf", "Emu", "Eraser", "Eskimo", "Exit"], "sound": "/e/"},
    "F": {"words": ["Fish", "Frog", "Fox", "Fire", "Flower", "Flag", "Fan", "Farm", "Feather", "Fork", "Fairy", "Foot", "Fence", "Family", "Five"], "sound": "/f/"},
    "G": {"words": ["Goat", "Girl", "Guitar", "Gate", "Ghost", "Glass", "Glove", "Gold", "Goose", "Gorilla", "Grape", "Grass", "Gift", "Giraffe", "Glue"], "sound": "/g/"},
    "H": {"words": ["Hat", "House", "Horse", "Hand", "Heart", "Helicopter", "Hippo", "Honey", "Horn", "Hose", "Hammer", "Hair", "Half", "Halo", "Ham"], "sound": "/h/"},
    "I": {"words": ["Ice", "Igloo", "Island", "Iron", "Insect", "Idea", "Iguana", "Ink", "Iris", "Item", "Ivy", "Iceberg", "Icon", "Idol", "Illusion"], "sound": "/i/"},
    "J": {"words": ["Jug", "Jam", "Jet", "Jelly", "Juice", "Jacket", "Jeep", "Jewel", "Jungle", "Jump", "Jigsaw", "Jester", "Judge", "Jar", "Joker"], "sound": "/j/"},
    "K": {"words": ["Kite", "Key", "Kangaroo", "King", "Koala", "Kitten", "Kiwi", "Knee", "Knife", "Knight", "Kettle", "Keyboard", "Kayak", "Ketchup", "Kid"], "sound": "/k/"},
    "L": {"words": ["Lion", "Leaf", "Lamp", "Lock", "Log", "Lemon", "Lake", "Leg", "Letter", "Lizard", "Ladder", "Ladybug", "Lamb", "Laptop", "Lasso"], "sound": "/l/"},
    "M": {"words": ["Monkey", "Moon", "Mouse", "Milk", "Map", "Man", "Mask", "Meat", "Melon", "Money", "Motorcycle", "Mountain", "Mushroom", "Music", "Muffin"], "sound": "/m/"},
    "N": {"words": ["Nest", "Net", "Nut", "Nail", "Nose", "Nurse", "Neck", "Needle", "Night", "Nine", "Ninja", "Note", "Number", "Notebook", "Noodle"], "sound": "/n/"},
    "O": {"words": ["Owl", "Octopus", "Orange", "Ocean", "Ostrich", "Oval", "Oven", "Ox", "Onion", "Otter", "Oar", "Oasis", "Oat", "Object", "Olive"], "sound": "/o/"},
    "P": {"words": ["Pig", "Pen", "Pizza", "Panda", "Pear", "Pencil", "Piano", "Pie", "Pineapple", "Pumpkin", "Penguin", "Parrot", "Peach", "Peacock", "Pearl"], "sound": "/p/"},
    "Q": {"words": ["Queen", "Quilt", "Quail", "Quarter", "Quartz", "Quiet", "Quill", "Quiz", "Quote", "Queue", "Quark", "Quest", "Quiver", "Quota", "Quack"], "sound": "/kw/"},
    "R": {"words": ["Rabbit", "Ring", "Robot", "Rain", "Rat", "Rainbow", "Rose", "Rock", "Rocket", "Roof", "Rooster", "Rope", "Ruler", "Rug", "Radio"], "sound": "/r/"},
    "S": {"words": ["Sun", "Star", "Snake", "Sock", "Shoe", "Snow", "Spoon", "Spider", "Squirrel", "Strawberry", "Submarine", "Swan", "Sword", "Sail", "Sand"], "sound": "/s/"},
    "T": {"words": ["Tiger", "Tree", "Turtle", "Train", "Tent", "Table", "Tooth", "Tomato", "Tractor", "Triangle", "Truck", "Tulip", "Turkey", "Taxi", "Tea"], "sound": "/t/"},
    "U": {"words": ["Umbrella", "Unicorn", "Uniform", "Urchin", "UFO", "Ukelele", "Uncle", "Under", "Up", "Urn", "Use", "Usher", "Utensil", "Umpire", "Universe"], "sound": "/u/"},
    "V": {"words": ["Van", "Vase", "Violin", "Volcano", "Vine", "Vest", "Vet", "Video", "Village", "Voice", "Vote", "Vulture", "Vacuum", "Valley", "Value"], "sound": "/v/"},
    "W": {"words": ["Water", "Whale", "Window", "Wolf", "Worm", "Wagon", "Wall", "Watch", "Web", "Wheel", "Wind", "Wing", "Wood", "Wool", "Wand"], "sound": "/w/"},
    "X": {"words": ["Xylophone", "X-ray", "Xenon", "Xerox", "Xmas", "Xiphias", "Xylem", "Xenops", "Xanthic", "Xebec", "Xenial", "Xyst", "Xanthippe", "Xenolith", "Xerophyte"], "sound": "/ks/"},
    "Y": {"words": ["Yak", "Yarn", "Yoyo", "Yacht", "Yard", "Yellow", "Yoga", "Yogurt", "Yolk", "Youth", "Yawn", "Year", "Yeast", "Yell", "Yield"], "sound": "/y/"},
    "Z": {"words": ["Zebra", "Zero", "Zoo", "Zipper", "Zigzag", "Zombie", "Zone", "Zucchini", "Zeppelin", "Zeus", "Zinc", "Zodiac", "Zookeeper", "Zoom", "Zephyr"], "sound": "/z/"}
}

def create_vocab_object(word, index, letter):
    word_lower = word.lower()
    return {
        "word": word,
        "syllables": 1 if len(word) < 5 else 2,
        "phonics": f"/{letter.lower()}/",
        "imageId": f"asset-{word_lower}",
        "outlineImageId": f"asset-{word_lower}-outline",
        "category": "General",
        "difficulty": 1 if index < 5 else (2 if index < 10 else 3),
        "keywords": [word_lower, letter.lower(), "alphabet"],
        "sentence": f"{word} starts with the letter {letter}.",
        "emoji": "✨"
    }

alphabet_dir = r"c:\Users\erpri\OneDrive\Desktop\worksheet wonder\04_Content_Database\Alphabet"

alphabet_index = []

for letter, data in letters_data.items():
    words = data["words"]
    hero = words[0:3]
    vocab = words[0:10]
    backup = words[10:15]
    
    vocab_objects = [create_vocab_object(w, i, letter) for i, w in enumerate(vocab)]
    backup_objects = [create_vocab_object(w, i, letter) for i, w in enumerate(backup)]
    
    letter_json = {
        "letter": letter,
        "uppercase": letter.upper(),
        "lowercase": letter.lower(),
        "phonicsSound": data["sound"],
        "formationSteps": [
            "Start at the top.",
            "Draw a line.",
            "Finish the shape."
        ],
        "difficulty": 1,
        "themeColor": "Blue",
        "heroWords": hero,
        "vocabulary": vocab_objects,
        "backupWords": backup_objects,
        "searchTags": [letter, letter.lower(), "alphabet", "preschool", "kindergarten", "phonics", "tracing", "writing", "letter-recognition", "early-years"],
        "curriculumReferences": ["EYFS-LIT-1", "CCSS.ELA.RF.K.1.D"],
        "teacherTips": f"Emphasize the {data['sound']} sound when introducing {letter}.",
        "parentTips": f"Look for objects starting with {letter} around your home!",
        "fineMotorObjective": "Trace continuous and broken lines with pencil control.",
        "phonicsObjective": f"Identify the initial {data['sound']} sound in spoken words."
    }
    
    filepath = os.path.join(alphabet_dir, f"{letter}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(letter_json, f, indent=2)
        
    alphabet_index.append({
        "letter": letter,
        "file": f"{letter}.json",
        "phonics": data["sound"]
    })

# Write the index
with open(os.path.join(alphabet_dir, "alphabet_index.json"), "w", encoding="utf-8") as f:
    json.dump(alphabet_index, f, indent=2)

print("Successfully generated 26 Alphabet JSON files and the index.")
