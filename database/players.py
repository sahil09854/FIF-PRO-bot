import random

PLAYERS = [
    # ICON
    {"name": "Ronaldo", "position": "FWD", "rating": 99, "pace": 89, "shooting": 99, "passing": 82, "dribbling": 95, "defending": 35, "physical": 88, "rarity": "ICON"},
    {"name": "Messi", "position": "FWD", "rating": 98, "pace": 81, "shooting": 95, "passing": 96, "dribbling": 99, "defending": 38, "physical": 65, "rarity": "ICON"},
    {"name": "Ronaldinho", "position": "FWD", "rating": 97, "pace": 82, "shooting": 92, "passing": 89, "dribbling": 99, "defending": 40, "physical": 70, "rarity": "ICON"},
    {"name": "Zidane", "position": "MID", "rating": 97, "pace": 76, "shooting": 88, "passing": 95, "dribbling": 97, "defending": 65, "physical": 75, "rarity": "ICON"},
    {"name": "Pele", "position": "FWD", "rating": 98, "pace": 87, "shooting": 97, "passing": 85, "dribbling": 96, "defending": 42, "physical": 78, "rarity": "ICON"},
    {"name": "Maradona", "position": "FWD", "rating": 97, "pace": 80, "shooting": 90, "passing": 88, "dribbling": 99, "defending": 38, "physical": 68, "rarity": "ICON"},
    {"name": "Lev Yashin", "position": "GK", "rating": 98, "pace": 55, "shooting": 15, "passing": 72, "dribbling": 25, "defending": 99, "physical": 88, "rarity": "ICON"},

    # GOLD RARE
    {"name": "Mbappe", "position": "FWD", "rating": 94, "pace": 99, "shooting": 93, "passing": 82, "dribbling": 95, "defending": 40, "physical": 78, "rarity": "GOLD_RARE"},
    {"name": "Haaland", "position": "FWD", "rating": 93, "pace": 89, "shooting": 97, "passing": 66, "dribbling": 80, "defending": 44, "physical": 92, "rarity": "GOLD_RARE"},
    {"name": "Vinicius Jr", "position": "FWD", "rating": 92, "pace": 97, "shooting": 86, "passing": 80, "dribbling": 95, "defending": 30, "physical": 68, "rarity": "GOLD_RARE"},
    {"name": "Bellingham", "position": "MID", "rating": 91, "pace": 80, "shooting": 86, "passing": 87, "dribbling": 88, "defending": 75, "physical": 85, "rarity": "GOLD_RARE"},
    {"name": "De Bruyne", "position": "MID", "rating": 91, "pace": 76, "shooting": 86, "passing": 98, "dribbling": 88, "defending": 64, "physical": 78, "rarity": "GOLD_RARE"},
    {"name": "Salah", "position": "FWD", "rating": 91, "pace": 94, "shooting": 90, "passing": 82, "dribbling": 92, "defending": 45, "physical": 77, "rarity": "GOLD_RARE"},
    {"name": "Alisson", "position": "GK", "rating": 91, "pace": 58, "shooting": 15, "passing": 78, "dribbling": 20, "defending": 91, "physical": 85, "rarity": "GOLD_RARE"},
    {"name": "Courtois", "position": "GK", "rating": 90, "pace": 55, "shooting": 12, "passing": 75, "dribbling": 18, "defending": 90, "physical": 88, "rarity": "GOLD_RARE"},
    {"name": "Van Dijk", "position": "DEF", "rating": 90, "pace": 78, "shooting": 60, "passing": 71, "dribbling": 65, "defending": 92, "physical": 90, "rarity": "GOLD_RARE"},
    {"name": "Modric", "position": "MID", "rating": 89, "pace": 74, "shooting": 76, "passing": 91, "dribbling": 90, "defending": 72, "physical": 66, "rarity": "GOLD_RARE"},
    {"name": "Benzema", "position": "FWD", "rating": 91, "pace": 79, "shooting": 92, "passing": 82, "dribbling": 88, "defending": 38, "physical": 78, "rarity": "GOLD_RARE"},
    {"name": "Lewandowski", "position": "FWD", "rating": 90, "pace": 78, "shooting": 95, "passing": 78, "dribbling": 85, "defending": 44, "physical": 82, "rarity": "GOLD_RARE"},
    {"name": "Neymar Jr", "position": "FWD", "rating": 90, "pace": 91, "shooting": 87, "passing": 87, "dribbling": 96, "defending": 36, "physical": 62, "rarity": "GOLD_RARE"},
    {"name": "Kante", "position": "MID", "rating": 89, "pace": 82, "shooting": 66, "passing": 78, "dribbling": 82, "defending": 92, "physical": 80, "rarity": "GOLD_RARE"},
    {"name": "Ter Stegen", "position": "GK", "rating": 89, "pace": 52, "shooting": 12, "passing": 80, "dribbling": 18, "defending": 89, "physical": 82, "rarity": "GOLD_RARE"},
    {"name": "Pedri", "position": "MID", "rating": 88, "pace": 75, "shooting": 76, "passing": 88, "dribbling": 90, "defending": 68, "physical": 64, "rarity": "GOLD_RARE"},
    {"name": "Rudiger", "position": "DEF", "rating": 88, "pace": 80, "shooting": 52, "passing": 68, "dribbling": 62, "defending": 88, "physical": 88, "rarity": "GOLD_RARE"},

    # GOLD
    {"name": "Osimhen", "position": "FWD", "rating": 87, "pace": 95, "shooting": 88, "passing": 65, "dribbling": 80, "defending": 38, "physical": 86, "rarity": "GOLD"},
    {"name": "Saka", "position": "FWD", "rating": 86, "pace": 88, "shooting": 82, "passing": 82, "dribbling": 86, "defending": 48, "physical": 68, "rarity": "GOLD"},
    {"name": "Bruno Fernandes", "position": "MID", "rating": 87, "pace": 72, "shooting": 82, "passing": 90, "dribbling": 84, "defending": 62, "physical": 72, "rarity": "GOLD"},
    {"name": "Rodri", "position": "MID", "rating": 89, "pace": 68, "shooting": 72, "passing": 88, "dribbling": 78, "defending": 90, "physical": 80, "rarity": "GOLD"},
    {"name": "Foden", "position": "MID", "rating": 87, "pace": 82, "shooting": 82, "passing": 86, "dribbling": 90, "defending": 58, "physical": 66, "rarity": "GOLD"},
    {"name": "Rashford", "position": "FWD", "rating": 85, "pace": 94, "shooting": 82, "passing": 74, "dribbling": 86, "defending": 38, "physical": 72, "rarity": "GOLD"},
    {"name": "Dybala", "position": "FWD", "rating": 85, "pace": 80, "shooting": 86, "passing": 80, "dribbling": 90, "defending": 38, "physical": 68, "rarity": "GOLD"},
    {"name": "Militao", "position": "DEF", "rating": 86, "pace": 82, "shooting": 52, "passing": 68, "dribbling": 68, "defending": 87, "physical": 84, "rarity": "GOLD"},
    {"name": "Donnarumma", "position": "GK", "rating": 88, "pace": 52, "shooting": 12, "passing": 74, "dribbling": 16, "defending": 88, "physical": 90, "rarity": "GOLD"},
    {"name": "Ederson", "position": "GK", "rating": 88, "pace": 58, "shooting": 14, "passing": 82, "dribbling": 18, "defending": 88, "physical": 84, "rarity": "GOLD"},
    {"name": "Cancelo", "position": "DEF", "rating": 86, "pace": 84, "shooting": 68, "passing": 84, "dribbling": 82, "defending": 82, "physical": 74, "rarity": "GOLD"},
    {"name": "Griezmann", "position": "FWD", "rating": 86, "pace": 78, "shooting": 85, "passing": 80, "dribbling": 84, "defending": 52, "physical": 74, "rarity": "GOLD"},
    {"name": "Havertz", "position": "MID", "rating": 84, "pace": 78, "shooting": 80, "passing": 78, "dribbling": 80, "defending": 60, "physical": 76, "rarity": "GOLD"},
    {"name": "Stones", "position": "DEF", "rating": 84, "pace": 72, "shooting": 54, "passing": 76, "dribbling": 72, "defending": 86, "physical": 78, "rarity": "GOLD"},

    # SILVER
    {"name": "Lookman", "position": "FWD", "rating": 82, "pace": 88, "shooting": 78, "passing": 70, "dribbling": 80, "defending": 38, "physical": 66, "rarity": "SILVER"},
    {"name": "Bernardo Silva", "position": "MID", "rating": 87, "pace": 76, "shooting": 78, "passing": 88, "dribbling": 88, "defending": 68, "physical": 66, "rarity": "SILVER"},
    {"name": "Tielemans", "position": "MID", "rating": 81, "pace": 70, "shooting": 74, "passing": 82, "dribbling": 78, "defending": 74, "physical": 70, "rarity": "SILVER"},
    {"name": "Zaha", "position": "FWD", "rating": 80, "pace": 88, "shooting": 74, "passing": 68, "dribbling": 82, "defending": 34, "physical": 70, "rarity": "SILVER"},
    {"name": "Pickford", "position": "GK", "rating": 81, "pace": 50, "shooting": 10, "passing": 68, "dribbling": 14, "defending": 81, "physical": 78, "rarity": "SILVER"},
    {"name": "Raya", "position": "GK", "rating": 82, "pace": 52, "shooting": 11, "passing": 72, "dribbling": 16, "defending": 82, "physical": 80, "rarity": "SILVER"},
    {"name": "Trippier", "position": "DEF", "rating": 83, "pace": 72, "shooting": 64, "passing": 80, "dribbling": 72, "defending": 80, "physical": 72, "rarity": "SILVER"},
    {"name": "Wan-Bissaka", "position": "DEF", "rating": 78, "pace": 82, "shooting": 42, "passing": 58, "dribbling": 68, "defending": 82, "physical": 72, "rarity": "SILVER"},

    # BRONZE
    {"name": "Eze", "position": "MID", "rating": 78, "pace": 82, "shooting": 74, "passing": 74, "dribbling": 80, "defending": 52, "physical": 68, "rarity": "BRONZE"},
    {"name": "Nketiah", "position": "FWD", "rating": 74, "pace": 82, "shooting": 74, "passing": 62, "dribbling": 72, "defending": 36, "physical": 72, "rarity": "BRONZE"},
    {"name": "Flekken", "position": "GK", "rating": 76, "pace": 46, "shooting": 9, "passing": 6
