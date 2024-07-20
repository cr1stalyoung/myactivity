import random


class ItemChance:

    @staticmethod
    async def random_item_first_case(interaction, controller):
        items = {
            "coin": {"probability": 0.15, "name_db": "ProfileModel", "name_column": "coin", "description": "100 Coins", "rarity": "common", "type": "coin", "case": "power"},
            "coins": {"probability": 0.1496, "name_db": "ProfileModel", "name_column": "coin", "description": "200 Coins", "rarity": "common", "type": "coins", "case": "power"},
            "card_raid": {"probability": 0.1495, "name_db": "CardModel", "name_column": "raid", "description": 'Card "Raid"', "rarity": "common", "type": "card", "case": "power"},
            "operator_raid": {"probability": 0.101, "name_db": "OperatorModel", "name_column": "ranger", "description": 'Operator "Ranger"', "rarity": "uncommon", "type": "operator", "case": "power"},
            "theme_raid": {"probability": 0.1, "name_db": "DecalModel", "name_column": "rangers", "description": 'Theme "Night raid"', "rarity": "uncommon", "type": "theme", "case": "power"},
            "card_shot": {"probability": 0.099, "name_db": "CardModel", "name_column": "shot", "description": 'Card "Good Job"', "rarity": "uncommon", "type": "card", "case": "power"},
            "operator_sheriff": {"probability": 0.05, "name_db": "OperatorModel", "name_column": "sheriff", "description": 'Operator "Sheriff"', "rarity": "mythical", "type": "operator", "case": "power"},
            "theme_sheriff": {"probability": 0.045, "name_db": "DecalModel", "name_column": "west", "description": 'Theme "West"', "rarity": "mythical", "type": "theme", "case": "power"},
            "card_zeus": {"probability": 0.038, "name_db": "CardModel", "name_column": "zeus", "description": 'Card "Zeus"', "rarity": "mythical", "type": "card", "case": "power"},
            "card_lags": {"probability": 0.035, "name_db": "CardModel", "name_column": "lags", "description": 'Card "System failure"', "rarity": "mythical", "type": "card", "case": "power"},
            "theme_zeus": {"probability": 0.03, "name_db": "DecalModel", "name_column": "maskoff", "description": 'Theme "mask-off"', "rarity": "mythical", "type": "theme", "case": "power"},
            "operator_imperator": {"probability": 0.0136, "name_db": "OperatorModel", "name_column": "imperator", "description": 'Operator "Emperor"', "rarity": "ancient", "type": "operator", "case": "power"},
            "theme_imperator": {"probability": 0.013, "name_db": "DecalModel", "name_column": "emperor", "description": 'Theme "Horse Spirit"', "rarity": "ancient", "type": "theme", "case": "power"},
            "operator_sinister": {"probability": 0.0129, "name_db": "OperatorModel", "name_column": "sinister", "description": 'Operator "Night Hunter"', "rarity": "ancient", "type": "operator", "case": "power"},
            "theme_sinister": {"probability": 0.0124, "name_db": "DecalModel", "name_column": "cyberstalker", "description": 'Theme "Inner demon of the night"', "rarity": "ancient", "type": "theme", "case": "power"},
            "operator_zeus": {"probability": 0.001, "name_db": "OperatorModel", "name_column": "zeus", "description": 'Operator "Zeus"', "rarity": "immortal", "type": "operator", "case": "power"}
        }
        probabilities = [item_data["probability"] for item_data in items.values()]
        sum_probabilities = sum(probabilities)
        random_number = random.uniform(0, sum_probabilities)
        upper_bound = 0
        for item, item_data in items.items():
            upper_bound += item_data["probability"]
            if random_number < upper_bound:
                if item_data["type"] == "coin":
                    await controller.get_case_coin(interaction.guild.id, interaction.user.id, 100, "first_case")
                elif item_data["type"] == "coins":
                    await controller.get_case_coin(interaction.guild.id, interaction.user.id, 200, "first_case")
                else:
                    await controller.get_case_item(interaction.guild.id, interaction.user.id, "first_case", item_data["name_db"], item_data["name_column"])
                return item, item_data["description"], item_data["rarity"], item_data["type"], item_data["case"]

    @staticmethod
    async def random_item_second_case(interaction, controller):
        items = {
            "coin": {"probability": 0.13, "name_db": "ProfileModel", "name_column": "coin", "description": "100 Coins", "rarity": "common", "type": "coin", "case": "gold_rush"},
            "coins": {"probability": 0.1196, "name_db": "ProfileModel", "name_column": "coin", "description": "200 Coins", "rarity": "common", "type": "coins", "case": "gold_rush"},
            "card_rich": {"probability": 0.1195, "name_db": "CardModel", "name_column": "richmedium", "description": 'Card "Rich"', "rarity": "common", "type": "card", "case": "gold_rush"},
            "card_wtf": {"probability": 0.101, "name_db": "CardModel", "name_column": "wtf", "description": 'Card "WTF"', "rarity": "uncommon", "type": "card", "case": "gold_rush"},
            "card_dangerous": {"probability": 0.06, "name_db": "CardModel", "name_column": "dangerous", "description": 'Card "Dangerous"', "rarity": "uncommon", "type": "card", "case": "gold_rush"},
            "card_accurate": {"probability": 0.059, "name_db": "CardModel", "name_column": "accurate", "description": 'Card "Gold Rush"', "rarity": "uncommon", "type": "card", "case": "gold_rush"},
            "theme_classified": {"probability": 0.098, "name_db": "DecalModel", "name_column": "classified", "description": 'Theme "Classified"', "rarity": "uncommon", "type": "theme", "case": "gold_rush"},
            "operator_whimsy": {"probability": 0.097, "name_db": "OperatorModel", "name_column": "whimsy", "description": 'Operator "whimsy"', "rarity": "uncommon", "type": "operator", "case": "gold_rush"},
            "theme_classy": {"probability": 0.038, "name_db": "DecalModel", "name_column": "classy", "description": 'Theme "Classy"', "rarity": "mythical", "type": "theme", "case": "gold_rush"},
            "theme_leaves": {"probability": 0.025, "name_db": "DecalModel", "name_column": "leaves", "description": 'Theme "You are happy"', "rarity": "mythical", "type": "theme", "case": "gold_rush"},
            "theme_infographic": {"probability": 0.02, "name_db": "DecalModel", "name_column": "infographic", "description": 'Theme "Infographic"', "rarity": "mythical", "type": "theme", "case": "gold_rush"},
            "operator_popmaster": {"probability": 0.0136, "name_db": "OperatorModel", "name_column": "popmaster", "description": 'Operator "Popmaster"', "rarity": "mythical", "type": "operator", "case": "gold_rush"},
            "operator_coup": {"probability": 0.013, "name_db": "OperatorModel", "name_column": "coup", "description": 'Operator "Coup"', "rarity": "ancient", "type": "operator", "case": "gold_rush"},
            "operator_smoky": {"probability": 0.0129, "name_db": "OperatorModel", "name_column": "smoky", "description": 'Operator "Smoky"', "rarity": "ancient", "type": "operator", "case": "gold_rush"},
            "operator_king": {"probability": 0.0124, "name_db": "OperatorModel", "name_column": "king", "description": 'Operator "King"', "rarity": "ancient", "type": "operator", "case": "gold_rush"},
            "theme_cryptoinvestor": {"probability": 0.001, "name_db": "DecalModel", "name_column": "cryptoinvestor", "description": 'Theme "Crypto investor"', "rarity": "immortal", "type": "theme", "case": "gold_rush"}
        }
        probabilities = [item_data["probability"] for item_data in items.values()]
        sum_probabilities = sum(probabilities)
        random_number = random.uniform(0, sum_probabilities)
        upper_bound = 0
        for item, item_data in items.items():
            upper_bound += item_data["probability"]
            if random_number < upper_bound:
                if item_data["type"] == "coin":
                    await controller.get_case_coin(interaction.guild.id, interaction.user.id, 100, "first_case")
                elif item_data["type"] == "coins":
                    await controller.get_case_coin(interaction.guild.id, interaction.user.id, 200, "first_case")
                else:
                    await controller.get_case_item(interaction.guild.id, interaction.user.id, "second_case", item_data["name_db"], item_data["name_column"])
                return item, item_data["description"], item_data["rarity"], item_data["type"], item_data["case"]

    @staticmethod
    async def random_item_third_case(interaction, controller):
            items = {
                "coin": {"probability": 0.2385, "name_db": "ProfileModel", "name_column": "coin", "description": "100 Coins", "rarity": "common", "type": "coin", "case": "gs"},
                "coins": {"probability": 0.1096, "name_db": "ProfileModel", "name_column": "coin", "description": "200 Coins", "rarity": "common", "type": "coins", "case": "gs"},
                "card_cybergirl": {"probability": 0.1095, "name_db": "CardModel", "name_column": "cybergirl", "description": 'Card "Cyber girl"', "rarity": "common", "type": "card", "case": "gs"},
                "card_neonmeet": {"probability": 0.109, "name_db": "CardModel", "name_column": "neonmeet", "description": 'Card "Neon"', "rarity": "uncommon", "type": "card", "case": "gs"},
                "theme_youready": {"probability": 0.06, "name_db": "DecalModel", "name_column": "youready", "description": 'Theme "Are You Ready?"', "rarity": "uncommon", "type": "theme", "case": "gs"},
                "operator_cupid": {"probability": 0.099, "name_db": "OperatorModel", "name_column": "cupid", "description": 'Operator "Cupid"', "rarity": "uncommon", "type": "operator", "case": "gs"},
                "card_leaves": {"probability": 0.098, "name_db": "CardModel", "name_column": "leaves", "description": 'Card "Leaves of happiness"', "rarity": "mythical", "type": "card", "case": "gs"},
                "theme_shadow": {"probability": 0.059, "name_db": "DecalModel", "name_column": "shadow", "description": 'Theme "Shadow"', "rarity": "mythical", "type": "theme", "case": "gs"},
                "theme_shark": {"probability": 0.038, "name_db": "DecalModel", "name_column": "shark", "description": 'Theme "Shark"', "rarity": "mythical", "type": "theme", "case": "gs"},
                "operator_ghost": {"probability": 0.025, "name_db": "OperatorModel", "name_column": "ghost", "description": 'Operator "Ghost"', "rarity": "mythical", "type": "operator", "case": "gs"},
                "operator_izzy": {"probability": 0.0136, "name_db": "OperatorModel", "name_column": "izzy", "description": 'Operator "Izzy"', "rarity": "mythical", "type": "operator", "case": "gs"},
                "theme_galaxy": {"probability": 0.013, "name_db": "DecalModel", "name_column": "galaxy", "description": 'Theme "Galaxy"', "rarity": "ancient", "type": "theme", "case": "gs"},
                "operator_mind": {"probability": 0.0129, "name_db": "OperatorModel", "name_column": "mind", "description": 'Operator "Galactic mind"', "rarity": "ancient", "type": "operator", "case": "gs"},
                "operator_outbroken": {"probability": 0.0124, "name_db": "OperatorModel", "name_column": "outbroken", "description": 'Operator "Outbroken"', "rarity": "ancient", "type": "operator", "case": "gs"},
                "theme_outbroken": {"probability": 0.001, "name_db": "DecalModel", "name_column": "outbroken", "description": 'Theme "Anomaly"', "rarity": "immortal", "type": "theme", "case": "gs"}
            }
            probabilities = [item_data["probability"] for item_data in items.values()]
            sum_probabilities = sum(probabilities)
            random_number = random.uniform(0, sum_probabilities)
            upper_bound = 0
            for item, item_data in items.items():
                upper_bound += item_data["probability"]
                if random_number < upper_bound:
                    if item_data["type"] == "coin":
                        await controller.get_case_coin(interaction.guild.id, interaction.user.id, 100, "first_case")
                    elif item_data["type"] == "coins":
                        await controller.get_case_coin(interaction.guild.id, interaction.user.id, 200, "first_case")
                    else:
                        await controller.get_case_item(interaction.guild.id, interaction.user.id, "third_case", item_data["name_db"], item_data["name_column"])
                    return item, item_data["description"], item_data["rarity"], item_data["type"], item_data["case"]

    @staticmethod
    async def random_item_fourth_case(interaction, controller):
            items = {
                "abomination": {"probability": 0.2385, "name_db": "CardModel", "name_column": "abomination", "description": 'Card "Abomination"', "rarity": "uncommon", "type": "card", "case": "hunting"},
                "zombie_nuke": {"probability": 0.1096, "name_db": "CardModel", "name_column": "zombie_nuke", "description": 'Card "Zombie Nuke"', "rarity": "uncommon", "type": "card", "case": "hunting"},
                "hard_work": {"probability": 0.1095, "name_db": "CardModel", "name_column": "hard_work", "description": 'Card "Hard work"', "rarity": "uncommon", "type": "card", "case": "hunting"},
                "cave": {"probability": 0.109, "name_db": "CardModel", "name_column": "cave", "description": 'Card "Cave"', "rarity": "uncommon", "type": "card", "case": "hunting"},
                "perk": {"probability": 0.06, "name_db": "DecalModel", "name_column": "perk", "description": 'Theme "Perk"', "rarity": "uncommon", "type": "theme", "case": "hunting"},
                "perks": {"probability": 0.099, "name_db": "CardModel", "name_column": "perks", "description": 'Card "Perks"', "rarity": "mythical", "type": "card", "case": "hunting"},
                "crystal_clear": {"probability": 0.098, "name_db": "CardModel", "name_column": "crystal_clear", "description": 'Card "Crystal Clear"', "rarity": "mythical", "type": "card", "case": "hunting"},
                "zombie_hunt": {"probability": 0.059, "name_db": "CardModel", "name_column": "zombie_hunt", "description": 'Card "Zombie Hunt"', "rarity": "mythical", "type": "card", "case": "hunting"},
                "zombie_mastery": {"probability": 0.038, "name_db": "CardModel", "name_column": "zombie_mastery", "description": 'Card "Zombie Mastery"', "rarity": "mythical", "type": "card", "case": "hunting"},
                "ethereal": {"probability": 0.025, "name_db": "CardModel", "name_column": "ethereal", "description": 'Card "Ethereal"', "rarity": "mythical", "type": "card", "case": "hunting"},
                "medusa": {"probability": 0.0136, "name_db": "DecalModel", "name_column": "medusa", "description": 'Theme "Medusa"', "rarity": "mythical", "type": "theme", "case": "hunting"},
                "anomaly": {"probability": 0.013, "name_db": "DecalModel", "name_column": "anomaly", "description": 'Theme "Anomaly"', "rarity": "mythical", "type": "theme", "case": "hunting"},
                "hunter": {"probability": 0.0129, "name_db": "OperatorModel", "name_column": "hunter", "description": 'Operator "Gold Hunter"', "rarity": "ancient", "type": "operator", "case": "hunting"},
                "coral": {"probability": 0.0124, "name_db": "OperatorModel", "name_column": "coral", "description": 'Operator "Zombie-Coral"', "rarity": "ancient", "type": "operator", "case": "hunting"},
                "jellyfish": {"probability": 0.001, "name_db": "OperatorModel", "name_column": "jellyfish", "description": 'Operator "Jellyfish"', "rarity": "ancient", "type": "operator", "case": "hunting"}
            }
            probabilities = [item_data["probability"] for item_data in items.values()]
            sum_probabilities = sum(probabilities)
            random_number = random.uniform(0, sum_probabilities)
            upper_bound = 0
            for item, item_data in items.items():
                upper_bound += item_data["probability"]
                if random_number < upper_bound:
                    await controller.get_case_item(interaction.guild.id, interaction.user.id, "fourth_case", item_data["name_db"], item_data["name_column"])
                    return item, item_data["description"], item_data["rarity"], item_data["type"], item_data["case"]

    @staticmethod
    async def random_item_fifth_case(interaction, controller):
            items = {
                "happy_day": {"probability": 0.2385, "name_db": "CardModel", "name_column": "happy_day", "description": 'Card "Happy Day"', "rarity": "common", "type": "card", "case": "toxic"},
                "friday": {"probability": 0.1096, "name_db": "CardModel", "name_column": "friday", "description": 'Card "Friday under beer"', "rarity": "common", "type": "card", "case": "toxic"},
                "crazy_girl": {"probability": 0.1095, "name_db": "CardModel", "name_column": "crazy_girl", "description": 'Card "ANIME?"', "rarity": "common", "type": "card", "case": "toxic"},
                "cyborg": {"probability": 0.109, "name_db": "CardModel", "name_column": "cyborg", "description": 'Card "Cyborg"', "rarity": "common", "type": "card", "case": "toxic"},
                "contract": {"probability": 0.06, "name_db": "CardModel", "name_column": "contract", "description": 'Theme "Contract"', "rarity": "uncommon", "type": "card", "case": "toxic"},
                "stats": {"probability": 0.099, "name_db": "CardModel", "name_column": "stats", "description": 'Card "I play well"', "rarity": "uncommon", "type": "card", "case": "toxic"},
                "hot": {"probability": 0.098, "name_db": "CardModel", "name_column": "hot", "description": 'Card "HOT"', "rarity": "uncommon", "type": "card", "case": "toxic"},
                "tilt": {"probability": 0.059, "name_db": "CardModel", "name_column": "tilt", "description": 'Card "MAX Tilt"', "rarity": "mythical", "type": "card", "case": "toxic"},
                "smoke": {"probability": 0.038, "name_db": "CardModel", "name_column": "smoke", "description": 'Card "Give`em the smoke"', "rarity": "mythical", "type": "card", "case": "toxic"},
                "anime": {"probability": 0.025, "name_db": "DecalModel", "name_column": "anime", "description": 'Theme "Good Theme"', "rarity": "mythical", "type": "theme", "case": "toxic"},
                "secret": {"probability": 0.0136, "name_db": "DecalModel", "name_column": "secret", "description": 'Theme "gold isn`t always good"', "rarity": "mythical", "type": "theme", "case": "toxic"},
                "rabbit": {"probability": 0.013, "name_db": "OperatorModel", "name_column": "rabbit", "description": 'Operator "Rabbit"', "rarity": "mythical", "type": "operator", "case": "toxic"},
                "snow_queen": {"probability": 0.0129, "name_db": "OperatorModel", "name_column": "snow_queen", "description": 'Operator "Snow Queen"', "rarity": "ancient", "type": "operator", "case": "toxic"},
                "experiment": {"probability": 0.0124, "name_db": "DecalModel", "name_column": "experiment", "description": 'Theme "Experiment"', "rarity": "ancient", "type": "theme", "case": "toxic"},
                "toxic": {"probability": 0.001, "name_db": "OperatorModel", "name_column": "toxic", "description": 'Operator " I`m Toxic"', "rarity": "ancient", "type": "operator", "case": "toxic"}
            }
            probabilities = [item_data["probability"] for item_data in items.values()]
            sum_probabilities = sum(probabilities)
            random_number = random.uniform(0, sum_probabilities)
            upper_bound = 0
            for item, item_data in items.items():
                upper_bound += item_data["probability"]
                if random_number < upper_bound:
                    await controller.get_case_item(interaction.guild.id, interaction.user.id, "fifth_case", item_data["name_db"], item_data["name_column"])
                    return item, item_data["description"], item_data["rarity"], item_data["type"], item_data["case"]

    @staticmethod
    async def random_item_sixth_case(interaction, controller):
        items = {
            "hi": {"probability": 0.15, "name_db": "CardModel", "name_column": "hi", "description": 'Card "Hi World"', "rarity": "common", "type": "card", "case": "verdansk"},
            "pure_right": {"probability": 0.1496, "name_db": "CardModel", "name_column": "pure_right", "description": 'Card "Pure Right"', "rarity": "common", "type": "card", "case": "verdansk"},
            "champion": {"probability": 0.1495, "name_db": "CardModel", "name_column": "champion", "description": 'Card "Champion"', "rarity": "common", "type": "card", "case": "verdansk"},
            "friendship": {"probability": 0.101, "name_db": "CardModel", "name_column": "friendship", "description": 'Card "Friendship"', "rarity": "common", "type": "card", "case": "verdansk"},
            "angry": {"probability": 0.1, "name_db": "CardModel", "name_column": "angry", "description": 'Card "Angry"', "rarity": "common", "type": "card", "case": "verdansk"},
            "jump": {"probability": 0.099, "name_db": "CardModel", "name_column": "jump", "description": 'Card "Let`s GO!"', "rarity": "uncommon", "type": "card", "case": "verdansk"},
            "victory": {"probability": 0.05, "name_db": "CardModel", "name_column": "victory", "description": 'Card "Victory"', "rarity": "uncommon", "type": "card", "case": "verdansk"},
            "unbreakable": {"probability": 0.045, "name_db": "CardModel", "name_column": "unbreakable", "description": 'Card "Unbreakable"', "rarity": "uncommon", "type": "card", "case": "verdansk"},
            "shadow_lord": {"probability": 0.038, "name_db": "CardModel", "name_column": "shadow_lord", "description": 'Card "Shadow Lord"', "rarity": "uncommon", "type": "card", "case": "verdansk"},
            "dune": {"probability": 0.035, "name_db": "CardModel", "name_column": "dune", "description": 'Card "Dune"', "rarity": "uncommon", "type": "card", "case": "verdansk"},
            "cyber_angry": {"probability": 0.03, "name_db": "CardModel", "name_column": "cyber_angry", "description": 'Card "Cyber Angry"', "rarity": "mythical", "type": "card", "case": "verdansk"},
            "cyberpunk": {"probability": 0.0136, "name_db": "CardModel", "name_column": "cyberpunk", "description": 'Card "Cyberpunk"', "rarity": "mythical", "type": "card", "case": "verdansk"},
            "portal": {"probability": 0.013, "name_db": "CardModel", "name_column": "portal", "description": 'Card "Portal"', "rarity": "mythical", "type": "card", "case": "verdansk"},
            "king": {"probability": 0.0129, "name_db": "CardModel", "name_column": "king", "description": 'Card "King"', "rarity": "mythical", "type": "card", "case": "verdansk"},
            "element": {"probability": 0.0124, "name_db": "CardModel", "name_column": "element", "description": 'Card "Element"', "rarity": "mythical", "type": "card", "case": "verdansk"},
            "verdansk": {"probability": 0.001, "name_db": "DecalModel", "name_column": "verdansk", "description": 'Theme "Verdansk?"', "rarity": "immortal", "type": "theme", "case": "verdansk"}
        }
        probabilities = [item_data["probability"] for item_data in items.values()]
        sum_probabilities = sum(probabilities)
        random_number = random.uniform(0, sum_probabilities)
        upper_bound = 0
        for item, item_data in items.items():
            upper_bound += item_data["probability"]
            if random_number < upper_bound:
                await controller.get_case_item(interaction.guild.id, interaction.user.id, "sixth_case", item_data["name_db"], item_data["name_column"])
                return item, item_data["description"], item_data["rarity"], item_data["type"], item_data["case"]
