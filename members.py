members = {
    "Nayeon": [
        "NAYEON",
        "NA",
        "NAYEONNIE",
        "BUNNY",
        "UNNIE"
        ],
    "Jeongyeon": [
        "JEONGYEON",
        "JEONG",
        "JEONGERS"
    ],
    "Momo" : [
        "MOMO",
        "MO",
        "MOMORING"
    ],
    "Sana" : [
        "SANA",
        "SA"
    ],
    "Jihyo" : [
        "JIHYO",
        "JI",
        "LEADER"
    ],
    "Mina" : [
        "MINA",
        "MI",
        "PENGUIN",
        "MINARI"
    ],
    "Dahyun" : [
        "DAHYUN",
        "DA",
        "DUBU",
        "TOFU"
    ],
    "Chaeyoung" : [
        "CHAEYOUNG",
        "CHAE",
        "CUB"
    ],
    "Tzuyu" : [
        "TZUYU",
        "TZU",
        "MAKNAE",
        "CHEWY"
    ]
}

def hasAllMembers(inList):
    return all(map(lambda x : set(x) & set(map(lambda x : x.upper(), inList)), members.values()))

def nickToName(inNick):
    inNick = inNick.upper()
    for name, nicks in members.items():
        for nick in nicks:
            if nick == inNick:
                return name
    return None
