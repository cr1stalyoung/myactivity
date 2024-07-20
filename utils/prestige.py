class Level:

    @staticmethod
    async def get_image(level):
        division_name = {
            (0, 5): ("level_1.png", 451),
            (6, 9): ("level_2.png", 451),
            (10, 15): ("level_3.png", 445),
            (16, 20): ("level_4.png", 445),
            (21, 25): ("level_5.png", 445),
            (26, 30): ("level_6.png", 445),
            (31, 35): ("level_7.png", 445),
            (36, 40): ("level_8.png", 445),
            (41, 45): ("level_9.png", 445),
            (46, 50): ("level_10.png", 445),
            (51, 75): ("level_11.png", 445),
            (76, 99): ("level_12.png", 445),
            (100, 125): ("level_13.png", 439),
            (126, 150): ("level_14.png", 439),
            (151, 175): ("level_15.png", 439),
            (176, 200): ("level_16.png", 439),
            (201, 225): ("level_17.png", 439),
            (226, 250): ("level_18.png", 439),
            (251, 275): ("level_19.png", 439),
            (276, 300): ("level_20.png", 439)
        }

        for range_, prestige in division_name.items():
            if range_[0] <= level <= range_[1]:
                return prestige
