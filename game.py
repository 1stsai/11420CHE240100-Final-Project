import random

class Dice:
    def __init__(self):
        self.values = [0, 0, 0, 0, 0] # 0 means unrolled/blank
        self.held = [False] * 5
        self.rolls_left = 3

    def roll(self):
        if self.rolls_left > 0:
            for i in range(5):
                if not self.held[i]:
                    self.values[i] = random.randint(1, 6)
            self.rolls_left -= 1

    def toggle_hold(self, index):
        if self.rolls_left < 3:
            self.held[index] = not self.held[index]

    def reset_turn(self):
        self.values = [0, 0, 0, 0, 0] 
        self.held = [False] * 5
        self.rolls_left = 3

class Scorecard:
    def __init__(self):
        self.categories = {
            "Ones": None, "Twos": None, "Threes": None, "Fours": None,
            "Fives": None, "Sixes": None, "Three of a Kind": None,
            "Four of a Kind": None, "Full House": None, "Small Straight": None,
            "Large Straight": None, "Yatzy": None, "Chance": None
        }

    def calculate_score(self, category, dice_values):
        if 0 in dice_values: return 0 

        match category:
            case "Ones":   return sum(val for val in dice_values if val == 1)
            case "Twos":   return sum(val for val in dice_values if val == 2)
            case "Threes": return sum(val for val in dice_values if val == 3)
            case "Fours":  return sum(val for val in dice_values if val == 4)
            case "Fives":  return sum(val for val in dice_values if val == 5)
            case "Sixes":  return sum(val for val in dice_values if val == 6) 
            case "Three of a Kind":
                if any(dice_values.count(val) >= 3 for val in set(dice_values)): return sum(dice_values)
                return 0
            case "Four of a Kind":
                if any(dice_values.count(val) >= 4 for val in set(dice_values)): return sum(dice_values)
                return 0
            case "Full House":
                counts = [dice_values.count(val) for val in set(dice_values)]
                if 2 in counts and 3 in counts: return 25 
                return 0
            case "Small Straight":
                ds = set(dice_values)
                if {1,2,3,4}.issubset(ds) or {2,3,4,5}.issubset(ds) or {3,4,5,6}.issubset(ds): return 30
                return 0
            case "Large Straight":
                ds = set(dice_values)
                if ds == {1,2,3,4,5} or ds == {2,3,4,5,6}: return 40
                return 0
            case "Yatzy":
                if any(dice_values.count(val) == 5 for val in set(dice_values)): return 50
                return 0
            case "Chance":
                return sum(dice_values)
            case _:
                return 0

    def record_score(self, category, dice_values):
        if 0 in dice_values: return False 

        if self.categories.get(category) is None:
            self.categories[category] = self.calculate_score(category, dice_values)
            return True
        return False
        
    def get_upper_score(self):
        upper_cats = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]
        return sum(self.categories[cat] for cat in upper_cats if self.categories[cat] is not None)
        
    def get_bonus(self):
        return 35 if self.get_upper_score() >= 63 else 0

    def get_total_score(self):
        base_score = sum(score for score in self.categories.values() if score is not None)
        return base_score + self.get_bonus()