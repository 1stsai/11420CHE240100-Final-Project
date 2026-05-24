import random
from game import Scorecard

class YatzyAgent:
    def __init__(self):
        self.dummy_scorecard = Scorecard()

    def get_action(self, dice, scorecard):
        if dice.rolls_left == 3: return "ROLL", None
        if dice.rolls_left == 0: return "SCORE", self._get_best_category(dice.values, scorecard)
        
        best_cat, best_score = self._evaluate_dice_state(dice.values, scorecard)
        if best_score >= 40: return "SCORE", best_cat

        best_hold = self._find_best_hold(dice.values, scorecard)
        return "HOLD", best_hold

    def _find_best_hold(self, current_values, scorecard):
        best_hold = [False] * 5
        best_ev = -1

        for i in range(32):
            hold_pattern = [(i >> j) & 1 == 1 for j in range(5)]
            ev = self._simulate_hold_ev(current_values, hold_pattern, scorecard)
            if ev > best_ev:
                best_ev = ev
                best_hold = hold_pattern
                
        return best_hold

    def _simulate_hold_ev(self, values, hold, scorecard, iterations=20):
        total_score = 0
        for _ in range(iterations):
            sim_values = [values[i] if hold[i] else random.randint(1, 6) for i in range(5)]
            _, score = self._evaluate_dice_state(sim_values, scorecard)
            total_score += score
        return total_score / iterations

    def _evaluate_dice_state(self, values, scorecard):
        best_cat = None
        max_score = -1
        current_upper = scorecard.get_upper_score()
        upper_cats = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]
        
        for cat, current_score in scorecard.categories.items():
            if current_score is None:
                val = self.dummy_scorecard.calculate_score(cat, values)
                heuristic_val = val
                
                if cat == "Chance" and val < 20: heuristic_val -= 10 
                    
                if cat in upper_cats:
                    pars = {"Ones": 3, "Twos": 6, "Threes": 9, "Fours": 12, "Fives": 15, "Sixes": 18}
                    if val >= pars[cat]:
                        heuristic_val += 8 
                        if current_upper < 63 and (current_upper + val) >= 63:
                            heuristic_val += 35 
                    else:
                        heuristic_val -= 5 

                if heuristic_val > max_score:
                    max_score = heuristic_val
                    best_cat = cat
                    
        return best_cat, max_score

    def _get_best_category(self, dice_values, scorecard):
        best_cat, max_score = self._evaluate_dice_state(dice_values, scorecard)
        if max_score > 0: return best_cat
            
        # BUG FIX: Expanded sacrifice list to all categories to prevent "None" loop
        sacrifices = ["Yatzy", "Large Straight", "Small Straight", "Four of a Kind", "Three of a Kind", "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "Full House", "Chance"]
        for sac in sacrifices:
            if scorecard.categories[sac] is None: return sac
            
        # Ultimate fail-safe: just pick the first available empty slot
        for cat, val in scorecard.categories.items():
            if val is None: return cat
            
        return best_cat

class RuleBasedAgent1(YatzyAgent):
    def get_action(self, dice, scorecard):
        if dice.rolls_left == 3: return "ROLL", None
        if dice.rolls_left == 0: return "SCORE", self._get_best_category(dice.values, scorecard)

        counts = {v: dice.values.count(v) for v in set(dice.values)}
        
        pairs = [v for v, c in counts.items() if c >= 2]
        if len(pairs) >= 2 and scorecard.categories["Full House"] is None:
            hold = [val in pairs[:2] for val in dice.values]
            if sum(hold) == 4: return "HOLD", hold

        for high_val in [6, 5, 4]:
            if counts.get(high_val, 0) >= 2:
                return "HOLD", [val == high_val for val in dice.values]

        for low_val in [3, 2, 1]:
            if counts.get(low_val, 0) >= 2:
                return "HOLD", [val == low_val for val in dice.values]

        return super().get_action(dice, scorecard)

    def _get_best_category(self, dice_values, scorecard):
        counts = {v: dice_values.count(v) for v in set(dice_values)}
        failed_high_roll = False
        target_val = None
        
        for high_val in [4, 5, 6]:
            if counts.get(high_val, 0) == 2: 
                failed_high_roll = True
                target_val = high_val
                break

        if failed_high_roll:
            if scorecard.categories["Ones"] is None: return "Ones"
            if scorecard.categories["Twos"] is None: return "Twos"
            val_names = {4: "Fours", 5: "Fives", 6: "Sixes"}
            if scorecard.categories[val_names[target_val]] is None:
                return val_names[target_val]

        return super()._get_best_category(dice_values, scorecard)

class RuleBasedAgent2(YatzyAgent):
    def get_action(self, dice, scorecard):
        if dice.rolls_left == 3: return "ROLL", None
        if dice.rolls_left == 0: return "SCORE", self._get_best_category(dice.values, scorecard)

        counts = {v: dice.values.count(v) for v in set(dice.values)}
        pairs = [v for v, c in counts.items() if c >= 2]
        
        unique_vals = sorted(list(set(dice.values)))
        longest_seq, current_seq = [], []
        for v in unique_vals:
            if not current_seq or v == current_seq[-1] + 1:
                current_seq.append(v)
            else:
                if len(current_seq) > len(longest_seq): longest_seq = current_seq
                current_seq = [v]
        if len(current_seq) > len(longest_seq): longest_seq = current_seq

        if len(longest_seq) == 4 and scorecard.categories["Large Straight"] is None:
            hold = []
            held_vals = set()
            for v in dice.values:
                if v in longest_seq and v not in held_vals:
                    hold.append(True)
                    held_vals.add(v)
                else: hold.append(False)
            return "HOLD", hold
                
        if len(longest_seq) == 3 and dice.rolls_left == 2 and scorecard.categories["Small Straight"] is None:
            hold = []
            held_vals = set()
            for v in dice.values:
                if v in longest_seq and v not in held_vals:
                    hold.append(True)
                    held_vals.add(v)
                else: hold.append(False)
            return "HOLD", hold

        if len(pairs) >= 2 and dice.rolls_left == 2 and scorecard.categories["Full House"] is None:
            hold = [val in pairs[:2] for val in dice.values]
            if sum(hold) == 4: return "HOLD", hold

        return super().get_action(dice, scorecard)

    def _evaluate_dice_state(self, values, scorecard):
        best_cat, max_score = None, -1
        current_upper = scorecard.get_upper_score()
        total_sum = sum(values)
        upper_cats = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]
        
        for cat, current_score in scorecard.categories.items():
            if current_score is None:
                val = self.dummy_scorecard.calculate_score(cat, values)
                if val == 0 and cat != "Chance": continue 
                
                heuristic_val = val
                
                if cat == "Yatzy" and val == 50:
                    heuristic_val += 1000
                elif cat == "Large Straight" and val == 40:
                    heuristic_val += 800
                elif cat == "Four of a Kind" and val > 0:
                    if total_sum > 23: heuristic_val += 600
                    else: heuristic_val += 100 
                elif cat in upper_cats:
                    pars = {"Ones": 3, "Twos": 6, "Threes": 9, "Fours": 12, "Fives": 15, "Sixes": 18}
                    if val >= pars[cat]:
                        heuristic_val += 500 
                        if current_upper < 63 and (current_upper + val) >= 63:
                            heuristic_val += 200 
                    else:
                        heuristic_val -= 10 
                elif cat == "Full House" and val == 25:
                    heuristic_val += 400
                elif cat == "Small Straight" and val == 30:
                    heuristic_val += 300
                elif cat == "Three of a Kind" and val > 0:
                    if total_sum > 25: heuristic_val += 200
                    else: heuristic_val += 50

                if cat == "Chance" and val < 20: 
                    heuristic_val -= 10 

                if heuristic_val > max_score:
                    max_score, best_cat = heuristic_val, cat
                    
        # BUG FIX: Ensure we NEVER return None
        if best_cat is None:
            sacrifices = ["Yatzy", "Large Straight", "Small Straight", "Four of a Kind", "Three of a Kind", "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "Full House", "Chance"]
            for sac in sacrifices:
                if scorecard.categories[sac] is None: return sac, -1
            # Ultimate fail-safe
            for cat, val in scorecard.categories.items():
                if val is None: return cat, -1
                    
        return best_cat, max_score

    def _get_best_category(self, dice_values, scorecard):
        best_cat, max_score = self._evaluate_dice_state(dice_values, scorecard)
        return best_cat

class ReflexAgent:
    def __init__(self): self.dummy_scorecard = Scorecard()
    def get_action(self, dice, scorecard):
        if dice.rolls_left == 3: return "ROLL", None
        if dice.rolls_left == 0: return "SCORE", self._get_greedy_category(dice.values, scorecard)
        hold_pattern = [val >= 5 for val in dice.values]
        if all(hold_pattern): return "SCORE", self._get_greedy_category(dice.values, scorecard)
        return "HOLD", hold_pattern

    def _get_greedy_category(self, dice_values, scorecard):
        best_cat, max_score = None, -1
        for cat, current_val in scorecard.categories.items():
            if current_val is None:
                score = self.dummy_scorecard.calculate_score(cat, dice_values)
                if score >= max_score: max_score, best_cat = score, cat
        
        # Safe Fallback just in case
        if best_cat is None:
            for cat, val in scorecard.categories.items():
                if val is None: return cat
        return best_cat