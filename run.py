import pygame
import sys
import argparse
from game import Dice, Scorecard
from gui import YatzyGUI, WIDTH, HEIGHT, FPS
from agents import YatzyAgent, RuleBasedAgent, ReflexAgent

def get_agent(agent_name):
    """Helper to instantiate agents based on CLI string."""
    if agent_name == 'minimax': return YatzyAgent()
    elif agent_name == 'rule': return RuleBasedAgent()
    elif agent_name == 'reflex': return ReflexAgent()
    return ReflexAgent()

def run_simulation(num_games, p1_type, p2_type):
    print(f"\n{'='*50}\n DEBUG SESSION: {p1_type.upper()} vs {p2_type.upper()} ({num_games} Games)\n{'='*50}\n")
    
    p1_wins, p2_wins = 0, 0
    p1_total_score, p2_total_score = 0, 0
    
    agent_1 = get_agent(p1_type)
    agent_2 = get_agent(p2_type)

    for i in range(1, num_games + 1):
        dice, scorecards, current_player = Dice(), [Scorecard(), Scorecard()], 0
        
        while not all(s is not None for s in scorecards[0].categories.values()) or \
              not all(s is not None for s in scorecards[1].categories.values()):
            
            active_agent = agent_1 if current_player == 0 else agent_2
            active_scorecard = scorecards[current_player]
            action, value = active_agent.get_action(dice, active_scorecard)
            
            if action == "ROLL": 
                dice.roll()
            elif action == "HOLD":
                dice.held = value
                dice.roll()
            elif action == "SCORE":
                active_scorecard.record_score(value, dice.values)
                current_player = 1 - current_player
                dice.reset_turn()
        
        p1_total, p2_total = scorecards[0].get_total_score(), scorecards[1].get_total_score()
        p1_total_score += p1_total
        p2_total_score += p2_total
        
        winner = "P1" if p1_total > p2_total else ("P2" if p2_total > p1_total else "Tie")
        if p1_total > p2_total: p1_wins += 1
        elif p2_total > p1_total: p2_wins += 1
        print(f"Match {i:03}: {p1_type.upper()} [{p1_total:3}] vs {p2_type.upper()} [{p2_total:3}] -> Winner: {winner}")

    p1_avg, p2_avg = p1_total_score / num_games, p2_total_score / num_games
    print(f"\n{'='*50}\n FINAL STATS")
    print(f" P1 ({p1_type}) Wins: {p1_wins} | P2 ({p2_type}) Wins: {p2_wins} | Ties: {num_games - p1_wins - p2_wins}")
    print(f" P1 Win Rate: {(p1_wins/num_games)*100:.1f}%\n P1 Avg Score: {p1_avg:.1f} | P2 Avg Score: {p2_avg:.1f}\n{'='*50}\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Activate headless debug mode')
    parser.add_argument('--games', type=int, default=10, help='Number of games to simulate')
    parser.add_argument('--p1', type=str, choices=['reflex', 'minimax', 'rule'], default='rule', help='Agent type for Player 1')
    parser.add_argument('--p2', type=str, choices=['reflex', 'minimax', 'rule'], default='reflex', help='Agent type for Player 2')
    args = parser.parse_args()

    if args.debug:
        run_simulation(args.games, args.p1, args.p2)
        return

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Yatzy")
    clock = pygame.time.Clock()
    gui = YatzyGUI(screen)
    
    agents = {
        "AI_MINIMAX": YatzyAgent(),
        "AI_RULE": RuleBasedAgent()
    }
    
    state, game_mode = "MENU", "PVP"
    dice, scorecards = Dice(), [Scorecard(), Scorecard()], 
    current_player, last_ai_time = 0, 0

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            
            human_turn = (current_player == 0) or (current_player == 1 and game_mode == "PVP")
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action, value = gui.get_click_action(event.pos, state)
                
                if state == "MENU" and action == "START":
                    game_mode, state = value, "PLAYING"
                    dice.reset_turn()
                    scorecards = [Scorecard(), Scorecard()]
                    current_player = 0
                elif state == "END_SCREEN" and action == "MENU":
                    state = "MENU"
                elif state == "PLAYING" and human_turn:
                    if action == "ROLL": 
                        dice.roll()
                    elif action == "DIE": 
                        dice.toggle_hold(value)
                    elif action == "SCORE":
                        if scorecards[current_player].record_score(value, dice.values):
                            current_player = 1 - current_player
                            dice.reset_turn()
                            last_ai_time = pygame.time.get_ticks()

        if state == "PLAYING" and current_player == 1 and "AI" in game_mode:
            if current_time - last_ai_time > 1500:
                active_agent = agents[game_mode]
                action, value = active_agent.get_action(dice, scorecards[1])
                
                if action == "ROLL": 
                    dice.roll()
                    last_ai_time = pygame.time.get_ticks()
                elif action == "HOLD":
                    dice.held = value
                    gui.draw_game(dice, scorecards, current_player, game_mode)
                    pygame.display.flip()
                    pygame.time.delay(1200) 
                    dice.roll()
                    last_ai_time = pygame.time.get_ticks()
                elif action == "SCORE":
                    pygame.time.delay(800)
                    scorecards[1].record_score(value, dice.values)
                    current_player = 0
                    dice.reset_turn()

        if state == "MENU": gui.draw_menu()
        elif state == "PLAYING":
            gui.draw_game(dice, scorecards, current_player, game_mode)
            if all(s is not None for s in scorecards[0].categories.values()) and \
               all(s is not None for s in scorecards[1].categories.values()):
                state = "END_SCREEN"
        elif state == "END_SCREEN": gui.draw_end_screen(scorecards, game_mode)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()