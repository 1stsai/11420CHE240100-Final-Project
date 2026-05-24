import pygame

WIDTH, HEIGHT = 900, 640
FPS = 60

SCORE_BG = (250, 235, 205)     
MENU_BG = (252, 228, 172)      
DARK_BLUE = (27, 117, 161)     

P1_BOX = (4, 170, 210)         
P2_BOX = (231, 85, 78)         
P1_BG = (164, 218, 232)        
P2_BG = (242, 179, 174)        

DICE_UNROLLED = (95, 102, 113) 
WHITE, BLACK = (255, 255, 255), (40, 40, 40)
CYAN_HOLD = (0, 255, 255)      
YELLOW = (255, 215, 0)

class YatzyGUI:
    def __init__(self, screen):
        self.screen = screen
        self.dice_font = pygame.font.SysFont('arial', 48, bold=True)
        self.score_font = pygame.font.SysFont('arial', 24, bold=True)
        self.small_font = pygame.font.SysFont('arial', 14, bold=True)
        self.title_font = pygame.font.SysFont('arial', 64, bold=True)
        
        self.roll_btn = pygame.Rect(40, 150, 250, 60)
        self.dice_rects = [pygame.Rect(40 + (i * 70), 60, 60, 60) for i in range(5)]
        
        # 4 Buttons on Main Menu now
        self.pvp_btn = pygame.Rect(300, 160, 300, 60)
        self.ai_btn = pygame.Rect(300, 240, 300, 60)
        self.custom_ai_btn1 = pygame.Rect(300, 320, 300, 60)
        self.custom_ai_btn2 = pygame.Rect(300, 400, 300, 60)
        
        self.category_rects = {} 

    def draw_menu(self):
        self.screen.fill(MENU_BG)
        title = self.title_font.render("YATZY", True, BLACK)
        self.screen.blit(title, title.get_rect(center=(WIDTH//2, 100)))

        buttons = [
            (self.pvp_btn, "Player vs Player"),
            (self.ai_btn, "Player vs AI (Minimax)"),
            (self.custom_ai_btn1, "Player vs AI (Rule 1)"),
            (self.custom_ai_btn2, "Player vs AI (Rule 2)")
        ]
        
        for btn, text in buttons:
            pygame.draw.rect(self.screen, DARK_BLUE, btn, border_radius=10)
            rendered_text = self.score_font.render(text, True, WHITE)
            self.screen.blit(rendered_text, rendered_text.get_rect(center=btn.center))

    def draw_game(self, dice, scorecards, current_player, game_mode):
        current_bg = P1_BG if current_player == 0 else P2_BG
        current_btn_color = P1_BOX if current_player == 0 else P2_BOX
        
        self.screen.fill(current_bg)
        self.draw_dice(dice)
        
        if dice.rolls_left > 0 and not ("AI" in game_mode and current_player == 1):
            pygame.draw.rect(self.screen, current_btn_color, self.roll_btn, border_radius=10)
            btn_text = self.dice_font.render(f"ROLL  {dice.rolls_left}", True, WHITE)
            self.screen.blit(btn_text, btn_text.get_rect(center=self.roll_btn.center))

        turn_text = "Player 1's Turn" if current_player == 0 else ("AI's Turn" if "AI" in game_mode else "Player 2's Turn")
        indicator = self.score_font.render(turn_text, True, BLACK)
        self.screen.blit(indicator, (40, 240)) 

        p1_total = scorecards[0].get_total_score()
        p2_total = scorecards[1].get_total_score()
        p2_name = "AI" if "AI" in game_mode else "P2"
        
        score_title = self.score_font.render("Current Totals:", True, BLACK)
        self.screen.blit(score_title, (40, 400)) 
        
        p1_display = self.score_font.render(f"P1: {p1_total} pts", True, BLACK)
        self.screen.blit(p1_display, (40, 440))
        p2_display = self.score_font.render(f"{p2_name}: {p2_total} pts", True, BLACK)
        self.screen.blit(p2_display, (40, 470))

        self.draw_scorecard(scorecards, current_player, game_mode)

    def draw_dice(self, dice):
        for i in range(5):
            rect = self.dice_rects[i]
            val = dice.values[i]
            
            if val == 0:
                pygame.draw.rect(self.screen, DICE_UNROLLED, rect, border_radius=8)
                cx, cy = rect.center
                star_points = [(cx, cy-12), (cx+3, cy-3), (cx+12, cy), (cx+3, cy+3), 
                               (cx, cy+12), (cx-3, cy+3), (cx-12, cy), (cx-3, cy-3)]
                pygame.draw.polygon(self.screen, WHITE, star_points)
            else:
                pygame.draw.rect(self.screen, WHITE, rect, border_radius=8)
                cx, cy = rect.center
                offset = 14
                pos = []
                if val in [1, 3, 5]: pos.append((cx, cy)) 
                if val in [2, 3, 4, 5, 6]: pos.extend([(cx-offset, cy-offset), (cx+offset, cy+offset)]) 
                if val in [4, 5, 6]: pos.extend([(cx-offset, cy+offset), (cx+offset, cy-offset)]) 
                if val == 6: pos.extend([(cx-offset, cy), (cx+offset, cy)]) 
                for p in pos: pygame.draw.circle(self.screen, BLACK, p, 5)

                if dice.held[i]:
                    pygame.draw.rect(self.screen, CYAN_HOLD, rect, width=5, border_radius=8)
                else:
                    pygame.draw.rect(self.screen, BLACK, rect, width=2, border_radius=8)

    def draw_category_icon(self, category, x, y):
        size = 34
        rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(self.screen, WHITE, rect, border_radius=6)
        pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=6)
        cx, cy = rect.center
        
        vals = {"Ones":1, "Twos":2, "Threes":3, "Fours":4, "Fives":5, "Sixes":6}
        if category in vals:
            val = vals[category]
            off = 8
            pos = []
            if val in [1,3,5]: pos.append((cx, cy))
            if val in [2,3,4,5,6]: pos.extend([(cx-off, cy-off), (cx+off, cy+off)])
            if val in [4,5,6]: pos.extend([(cx-off, cy+off), (cx+off, cy-off)])
            if val == 6: pos.extend([(cx-off, cy), (cx+off, cy)])
            for p in pos: pygame.draw.circle(self.screen, BLACK, p, 3)
            
        elif category == "Three of a Kind":
            txt = self.score_font.render("3X", True, BLACK)
            self.screen.blit(txt, txt.get_rect(center=(cx, cy)))
        elif category == "Four of a Kind":
            txt = self.score_font.render("4X", True, BLACK)
            self.screen.blit(txt, txt.get_rect(center=(cx, cy)))
        elif category == "Full House":
            pygame.draw.polygon(self.screen, BLACK, [(cx, cy-10), (cx-10, cy), (cx+10, cy)]) 
            pygame.draw.rect(self.screen, BLACK, (cx-8, cy, 16, 10)) 
            pygame.draw.rect(self.screen, WHITE, (cx-3, cy+4, 6, 6)) 
        elif category == "Small Straight":
            for i in range(3):
                pygame.draw.rect(self.screen, WHITE, (cx-10 + i*4, cy-8 + i*3, 12, 16), border_radius=2)
                pygame.draw.rect(self.screen, BLACK, (cx-10 + i*4, cy-8 + i*3, 12, 16), 1, border_radius=2)
        elif category == "Large Straight":
            for i in range(4):
                pygame.draw.rect(self.screen, WHITE, (cx-12 + i*4, cy-10 + i*4, 12, 16), border_radius=2)
                pygame.draw.rect(self.screen, BLACK, (cx-12 + i*4, cy-10 + i*4, 12, 16), 1, border_radius=2)
        elif category == "Yatzy":
            txt = self.small_font.render("YATZY", True, YELLOW)
            txt_bg = self.small_font.render("YATZY", True, BLACK)
            self.screen.blit(txt_bg, txt_bg.get_rect(center=(cx+1, cy+1)))
            self.screen.blit(txt, txt.get_rect(center=(cx, cy)))
        elif category == "Chance":
            txt = self.score_font.render("?", True, DARK_BLUE)
            self.screen.blit(txt, txt.get_rect(center=(cx, cy)))

    def draw_scorecard(self, scorecards, current_player, game_mode):
        start_x, start_y = 390, 40
        pygame.draw.rect(self.screen, SCORE_BG, (start_x, start_y, 480, 560), border_radius=15)
        pygame.draw.rect(self.screen, BLACK, (start_x, start_y, 480, 560), 3, border_radius=15)
        self.category_rects.clear()

        cats = list(scorecards[0].categories.keys())
        left_col = cats[:6]   
        right_col = cats[6:]  

        self._draw_column(scorecards, left_col, start_x + 20, start_y + 20)
        pygame.draw.line(self.screen, P2_BOX, (start_x + 240, start_y + 20), (start_x + 240, start_y + 540), 4)
        self._draw_column(scorecards, right_col, start_x + 260, start_y + 20)

        bonus_y = start_y + 20 + (6 * 45)
        bonus_txt = self.score_font.render("BONUS", True, BLACK)
        self.screen.blit(bonus_txt, (start_x + 20, bonus_y + 10))
        bonus_val = self.score_font.render("+35", True, (130, 80, 160)) 
        self.screen.blit(bonus_val, (start_x + 110, bonus_y + 10))

    def _draw_column(self, scorecards, categories, x_start, y_start):
        for i, category in enumerate(categories):
            y_pos = y_start + (i * 45)
            
            self.category_rects[category] = pygame.Rect(x_start + 45, y_pos, 150, 36)
            self.draw_category_icon(category, x_start, y_pos)
            
            p1_rect = pygame.Rect(x_start + 45, y_pos, 60, 36)
            pygame.draw.rect(self.screen, P1_BOX, p1_rect, border_radius=6)
            s1 = str(scorecards[0].categories[category]) if scorecards[0].categories[category] is not None else ""
            if s1:
                t1 = self.score_font.render(s1, True, WHITE)
                self.screen.blit(t1, t1.get_rect(center=p1_rect.center))
                
            p2_rect = pygame.Rect(x_start + 115, y_pos, 60, 36)
            pygame.draw.rect(self.screen, P2_BOX, p2_rect, border_radius=6)
            s2 = str(scorecards[1].categories[category]) if scorecards[1].categories[category] is not None else ""
            if s2:
                t2 = self.score_font.render(s2, True, WHITE)
                self.screen.blit(t2, t2.get_rect(center=p2_rect.center))

    def draw_end_screen(self, scorecards, game_mode):
        self.screen.fill(MENU_BG)
        p1_total, p2_total = scorecards[0].get_total_score(), scorecards[1].get_total_score()
        
        winner_text = "Player 1 Wins!"
        if p2_total > p1_total: winner_text = "AI Wins!" if "AI" in game_mode else "Player 2 Wins!"
        elif p1_total == p2_total: winner_text = "It's a Tie!"
            
        title = self.title_font.render(winner_text, True, BLACK)
        self.screen.blit(title, title.get_rect(center=(WIDTH//2, 150)))
        
        p2_name = "AI" if "AI" in game_mode else "Player 2"
        s1_text = self.dice_font.render(f"Player 1 Score: {p1_total}", True, BLACK)
        s2_text = self.dice_font.render(f"{p2_name} Score: {p2_total}", True, BLACK)
        
        self.screen.blit(s1_text, s1_text.get_rect(center=(WIDTH//2, 250)))
        self.screen.blit(s2_text, s2_text.get_rect(center=(WIDTH//2, 320)))
        
        self.pvp_btn.center = (WIDTH//2, 450)
        pygame.draw.rect(self.screen, DARK_BLUE, self.pvp_btn, border_radius=10)
        btn_text = self.score_font.render("Return to Menu", True, WHITE)
        self.screen.blit(btn_text, btn_text.get_rect(center=self.pvp_btn.center))

    def get_click_action(self, pos, state):
        if state == "MENU":
            self.pvp_btn.topleft = (300, 160) 
            if self.pvp_btn.collidepoint(pos): return "START", "PVP"
            if self.ai_btn.collidepoint(pos): return "START", "AI_MINIMAX"
            if self.custom_ai_btn1.collidepoint(pos): return "START", "AI_RULE1"
            if self.custom_ai_btn2.collidepoint(pos): return "START", "AI_RULE2"
        elif state == "PLAYING":
            if self.roll_btn.collidepoint(pos): return "ROLL", None
            for i, rect in enumerate(self.dice_rects):
                if rect.collidepoint(pos): return "DIE", i
            for cat, rect in self.category_rects.items():
                if rect.collidepoint(pos): return "SCORE", cat
        elif state == "END_SCREEN":
            if self.pvp_btn.collidepoint(pos): return "MENU", None
        return None, None