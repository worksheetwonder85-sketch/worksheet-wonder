$jsonStr = @"
{
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
"@

$data = $jsonStr | ConvertFrom-Json
$baseDir = "c:\Users\erpri\OneDrive\Desktop\worksheet wonder\04_Content_Database\Alphabet"
$indexArr = @()

foreach ($letter in $data.psobject.properties) {
    $L = $letter.Name
    $val = $letter.Value
    
    $hero = $val.words[0..2]
    $vocabWords = $val.words[0..9]
    $backupWords = $val.words[10..14]
    
    $vocabObjs = @()
    for ($i = 0; $i -lt $vocabWords.Length; $i++) {
        $w = $vocabWords[$i]
        $w_l = $w.ToLower()
        $syl = if ($w.Length -lt 5) { 1 } else { 2 }
        $diff = if ($i -lt 5) { 1 } elseif ($i -lt 10) { 2 } else { 3 }
        
        $obj = [ordered]@{
            "word" = $w
            "syllables" = $syl
            "phonics" = "/$($L.ToLower())/"
            "imageId" = "asset-$w_l"
            "outlineImageId" = "asset-$w_l-outline"
            "category" = "General"
            "difficulty" = $diff
            "keywords" = @($w_l, $L.ToLower(), "alphabet")
            "sentence" = "$w starts with the letter $L."
            "emoji" = "✨"
        }
        $vocabObjs += $obj
    }
    
    $backupObjs = @()
    for ($i = 0; $i -lt $backupWords.Length; $i++) {
        $w = $backupWords[$i]
        $w_l = $w.ToLower()
        $syl = if ($w.Length -lt 5) { 1 } else { 2 }
        
        $obj = [ordered]@{
            "word" = $w
            "syllables" = $syl
            "phonics" = "/$($L.ToLower())/"
            "imageId" = "asset-$w_l"
            "outlineImageId" = "asset-$w_l-outline"
            "category" = "General"
            "difficulty" = 3
            "keywords" = @($w_l, $L.ToLower(), "alphabet")
            "sentence" = "$w starts with the letter $L."
            "emoji" = "✨"
        }
        $backupObjs += $obj
    }
    
    $letterJson = [ordered]@{
        "letter" = $L
        "uppercase" = $L.ToUpper()
        "lowercase" = $L.ToLower()
        "phonicsSound" = $val.sound
        "formationSteps" = @("Start at the top.", "Draw a line.", "Finish the shape.")
        "difficulty" = 1
        "themeColor" = "Blue"
        "heroWords" = $hero
        "vocabulary" = $vocabObjs
        "backupWords" = $backupObjs
        "searchTags" = @($L, $L.ToLower(), "alphabet", "preschool", "kindergarten", "phonics", "tracing", "writing", "letter-recognition", "early-years")
        "curriculumReferences" = @("EYFS-LIT-1", "CCSS.ELA.RF.K.1.D")
        "teacherTips" = "Emphasize the $($val.sound) sound when introducing $L."
        "parentTips" = "Look for objects starting with $L around your home!"
        "fineMotorObjective" = "Trace continuous and broken lines with pencil control."
        "phonicsObjective" = "Identify the initial $($val.sound) sound in spoken words."
    }
    
    $filePath = Join-Path $baseDir "$L.json"
    $letterJson | ConvertTo-Json -Depth 10 | Set-Content $filePath -Encoding UTF8
    
    $indexArr += [ordered]@{
        "letter" = $L
        "file" = "$L.json"
        "phonics" = $val.sound
    }
}

$indexArr | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $baseDir "alphabet_index.json") -Encoding UTF8
Write-Output "Successfully generated 26 Alphabet JSON files and alphabet_index.json"
