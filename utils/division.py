class Division:

    @staticmethod
    async def definition(score):
        division_name = {
            (0, 899): ("resources/rank/bronze.png", "#6d5344"),
            (900, 2099): ("resources/rank/silver.png", "#65605b"),
            (2100, 3599): ("resources/rank/gold.png", "#504832"),
            (3600, 5399): ("resources/rank/platinum.png", "#325049"),
            (5400, 7499): ("resources/rank/diamond.png", "#232939"),
            (7500, 9999): ("resources/rank/crimson.png", "#392327"),
            (10000, float("inf")): "iridescent"
        }

        for range_, rank in division_name.items():
            if range_[0] <= score <= range_[1]:
                return range_, rank

    @staticmethod
    async def definition_server(score):
        division_name = {
            (0, 899): "resources/ranking/bronze.png",
            (900, 2099): "resources/ranking/silver.png",
            (2100, 3599): "resources/ranking/gold.png",
            (3600, 5399): "resources/ranking/platinum.png",
            (5400, 7499): "resources/ranking/diamond.png",
            (7500, 9999): "resources/ranking/crimson.png",
            (10000, float("inf")): "resources/ranking/iridescent.png"
        }

        for range_, rank in division_name.items():
            if range_[0] <= score <= range_[1]:
                return rank

    @staticmethod
    async def change_world_rank(score):
        division_name = {
            (-9999, -1000): "resources/ranking/-1000.png",
            (-999, -100): "resources/ranking/-100.png",
            (-99, -10): "resources/ranking/-10.png",
            (-9, -1): "resources/ranking/-1.png",
            (0, 9): "resources/ranking/1.png",
            (10, 99): "resources/ranking/10.png",
            (100, 999): "resources/ranking/100.png",
            (1000, 9999): "resources/ranking/1000.png"
        }

        for range_, rank in division_name.items():
            if range_[0] <= score <= range_[1]:
                return rank

    @staticmethod
    async def minus(score):
        division_minus = {
            (0, 899): 0,
            (900, 2099): 3,
            (2100, 3599): 10,
            (3600, 5399): 12,
            (5400, 7499): 15,
            (7500, 9999): 18,
            (10000, 10999): 25,
            (11000, 14999): 40,
            (15000, 19999): 80,
            (20000, 29999): 100,
            (30000, float("inf")): 150
        }

        for range_, minus in division_minus.items():
            if range_[0] <= score <= range_[1]:
                return minus
