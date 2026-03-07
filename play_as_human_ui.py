import pygame
import math
import sys
import numpy as np
import tomllib

try:
    from env import Env
    from agent_class import AbstractAgent
    from utils import select_agents
except ImportError:
    print("CRITICAL: Requires 'env', 'agent_class', and 'utils' to be present.")
    sys.exit()


SCREEN_SIZE = (1600, 900)
BG_COLOR = (30, 33, 40)
TEXT_COLOR = (220, 220, 220)
ACCENT_COLOR = (255, 215, 0)
FPS = 60

PLAYER_COLORS = [
    (80, 200, 120),  # Human (Emerald)
    (255, 100, 100),  # Opponent 1 (Red)
    (100, 150, 255),  # Opponent 2 (Blue)
    (200, 100, 200),  # Violet
]


class InteractiveGame:
    def __init__(self, env, human_agent, opponents):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Interactive Mode")
        self.clock = pygame.time.Clock()

        # Game Logic Objects
        self.env = env
        self.human_agent = human_agent
        self.opponents = opponents
        self.all_agents = [human_agent] + opponents

        # map agent names to colors
        self.agent_colors = {
            a.name: PLAYER_COLORS[i % len(PLAYER_COLORS)]
            for i, a in enumerate(self.all_agents)
        }

        # Layout Data
        self.font_s = pygame.font.SysFont("Consolas", 20)
        self.font_m = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_l = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_xl = pygame.font.SysFont("Arial", 60, bold=True)

        # Calculate Positions
        self._calculate_layout()

        # Game State
        self.round_idx = 0
        self.current_allocations = [0] * self.env.num_fields  # User's current plan

        # Animation States
        self.state = "INPUT"  # INPUT, CALCULATE, DEPLOY, RESOLVE, NEXT_ROUND, END
        self.anim_progress = 0.0
        self.timer = 0

        # Visualizers for current round
        self.history_buffer = []  # Stores round results to animate
        self.round_winners = []

        # UI Elements
        self.submit_btn_rect = pygame.Rect(0, 0, 200, 60)
        self.submit_btn_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 40)

    def reset(self):
        self.env.reset()
        self.state = "INPUT"
        self.round_idx = 0
        self.current_allocations = [0] * self.env.num_fields
        self.history_buffer = []
        self.round_winners = []
        self.anim_progress = 0.0
        self.timer = 0

    def _calculate_layout(self):
        """Pre-calculate positions for fields and players"""
        W, H = SCREEN_SIZE

        # Player Headers (Top)
        self.player_positions = {}
        zone_w = W * 0.9
        start_x = (W - zone_w) / 2
        gap = zone_w / len(self.all_agents)

        for i, agent in enumerate(self.all_agents):
            cx = start_x + (gap * i) + (gap / 2)
            cy = H * 0.1
            self.player_positions[agent.name] = (cx, cy)

        # Battlefields (Center Grid)
        num_fields = self.env.num_fields
        cols = math.ceil(math.sqrt(num_fields))
        rows = math.ceil(num_fields / cols)

        field_area_w = W * 0.8
        field_area_h = H * 0.5
        field_start_x = (W - field_area_w) / 2
        field_start_y = H * 0.25 - 20

        self.field_positions = []
        cell_w = field_area_w / cols
        cell_h = field_area_h / rows
        self.field_radius = min(cell_w, cell_h) * 0.35

        for i in range(num_fields):
            r = i // cols
            c = i % cols
            cx = field_start_x + (c * cell_w) + (cell_w / 2)
            cy = field_start_y + (r * cell_h + (r * 40)) + (cell_h / 2)
            self.field_positions.append((cx, cy))

    def handle_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "INPUT":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    # Check Submit Button
                    if self.submit_btn_rect.collidepoint((mx, my)):
                        self.trigger_turn_calculation()
                        return

                    # Check Fields
                    state = self.env.get_state()
                    current_balance = state["balances"][self.human_agent.name]
                    current_committed = sum(self.current_allocations)
                    remaining = current_balance - current_committed

                    # Shift modifier for larger increments
                    keys = pygame.key.get_pressed()
                    increment = (
                        5 if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else 1
                    )

                    for i, (fx, fy) in enumerate(self.field_positions):
                        dist = math.hypot(mx - fx, my - fy)
                        if dist < self.field_radius:
                            # Left Click: Add
                            if event.button == 1:
                                to_add = min(increment, remaining)
                                self.current_allocations[i] += to_add

                            # Right Click: Remove
                            elif event.button == 3:
                                to_remove = min(increment, self.current_allocations[i])
                                self.current_allocations[i] -= to_remove

    def trigger_turn_calculation(self):
        """Runs the actual game logic step once user hits submit"""
        self.state = "CALCULATE"

        state = self.env.get_state()
        moves = {self.human_agent.name: self.current_allocations}

        for opp in self.opponents:
            try:
                move = opp.get_allocation(
                    current_balance=state["balances"][opp.name],
                    field_values=self.env.field_values,
                    num_fields=self.env.num_fields,
                    history=state["history"],
                    balances=state["balances"],
                    total_rounds=self.env.total_rounds,
                    current_round=self.round_idx + 1,
                )
                moves[opp.name] = move
            except Exception as e:
                print(f"Error getting move from {opp.name}: {e}")
                moves[opp.name] = [0] * self.env.num_fields  # Fallback

        new_state, winners = self.env.step(moves)

        self.last_round_data = new_state["history"][-1]
        self.last_round_winners = winners

        # Transition to Animation
        self.state = "DEPLOY"
        self.anim_progress = 0.0

    def update(self):
        if self.state == "DEPLOY":
            self.anim_progress += 0.02
            if self.anim_progress >= 1.0:
                self.anim_progress = 1.0
                self.state = "RESOLVE"
                self.timer = pygame.time.get_ticks()

        elif self.state == "RESOLVE":
            self.state = "NEXT_ROUND"

        elif self.state == "NEXT_ROUND":
            self.round_idx += 1
            if self.round_idx >= self.env.total_rounds:
                self.state = "END"
            else:
                # Reset for next input
                self.current_allocations = [0] * self.env.num_fields
                self.state = "INPUT"

    def draw_battlefields(self):
        for i, pos in enumerate(self.field_positions):
            # Base Circle
            color = (80, 80, 80)

            # Highlight winner if in RESOLVE state
            if self.state in ["RESOLVE", "NEXT_ROUND", "END"]:
                w_idx = self.last_round_winners[i]
                if w_idx != -1:  # Not a tie
                    winner_name = self.all_agents[w_idx].name
                    color = self.agent_colors[winner_name]
                    # Draw a glow
                    pygame.draw.circle(
                        self.screen, color, pos, self.field_radius + 8, 4
                    )

            pygame.draw.circle(self.screen, color, pos, self.field_radius)
            pygame.draw.circle(self.screen, (200, 200, 200), pos, self.field_radius, 2)

            # Value Label
            val_lbl = self.font_m.render(
                str(self.env.field_values[i]), True, (255, 255, 255)
            )
            self.screen.blit(val_lbl, val_lbl.get_rect(center=pos))

            # INPUT STATE: Show user current allocation
            if self.state == "INPUT":
                alloc = self.current_allocations[i]
                if alloc > 0:
                    # Draw green badge
                    badge_pos = (pos[0], pos[1] + self.field_radius + 20)
                    txt = self.font_m.render(f"+{alloc}", True, PLAYER_COLORS[0])
                    self.screen.blit(txt, txt.get_rect(center=badge_pos))

    def draw_troops_anim(self):
        """Animates troops moving from players to fields"""
        if self.state != "DEPLOY":
            return

        round_data = self.last_round_data

        for agent in self.all_agents:
            name = agent.name
            start_pos = self.player_positions[name]
            allocs = round_data[name]
            color = self.agent_colors[name]

            for f_idx, count in enumerate(allocs):
                if count <= 0:
                    continue

                end_pos = self.field_positions[f_idx]

                cx = start_pos[0] + (end_pos[0] - start_pos[0]) * self.anim_progress
                cy = start_pos[1] + (end_pos[1] - start_pos[1]) * self.anim_progress
                size = min(8 + count, 25)

                pygame.draw.circle(self.screen, color, (cx, cy), size)

                # Draw number inside if large enough
                if size > 12:
                    lbl = self.font_s.render(str(int(count)), True, (0, 0, 0))
                    self.screen.blit(lbl, lbl.get_rect(center=(cx, cy)))

    def draw_results_static(self):
        """Shows static troop counts on fields after animation"""
        if self.state not in ["RESOLVE", "NEXT_ROUND", "END"]:
            return

        round_data = self.last_round_data

        for f_idx, pos in enumerate(self.field_positions):
            # Gather who sent what
            troops_here = []
            for agent in self.all_agents:
                count = round_data[agent.name][f_idx]
                if count > 0:
                    troops_here.append((agent.name, count))

            if not troops_here:
                continue

            # Arrange them in a circle around the field
            orbit_radius = self.field_radius + 35
            angle_step = 360 / len(troops_here)

            for i, (name, count) in enumerate(troops_here):
                angle = math.radians(i * angle_step - 90)
                bx = pos[0] + orbit_radius * math.cos(angle)
                by = pos[1] + orbit_radius * math.sin(angle)

                color = self.agent_colors[name]
                pygame.draw.circle(self.screen, color, (bx, by), 15)

                lbl = self.font_s.render(str(int(count)), True, (0, 0, 0))
                self.screen.blit(lbl, lbl.get_rect(center=(bx, by)))

    def draw_hud(self):
        state = self.env.get_state()

        # Round Info
        round_txt = self.font_l.render(
            f"ROUND {self.round_idx + 1} / {self.env.total_rounds}", True, TEXT_COLOR
        )
        self.screen.blit(round_txt, (30, 30))

        # Player Stats
        for name, pos in self.player_positions.items():
            color = self.agent_colors[name]
            score = state["scores"][name]
            balance = state["balances"][name]

            # Name
            name_lbl = self.font_m.render(name, True, color)
            self.screen.blit(name_lbl, (pos[0] - 50, pos[1] - 70))

            # Stats Box
            rect = pygame.Rect(0, 0, 160, 70)
            rect.center = pos
            pygame.draw.rect(self.screen, (50, 54, 62), rect, border_radius=8)
            pygame.draw.rect(self.screen, color, rect, 2, border_radius=8)

            score_txt = self.font_s.render(f"Score: {score}", True, ACCENT_COLOR)
            bal_txt = self.font_s.render(f"Troops: {balance}", True, TEXT_COLOR)

            self.screen.blit(score_txt, (rect.x + 10, rect.y + 10))
            self.screen.blit(bal_txt, (rect.x + 10, rect.y + 35))

        if self.state == "INPUT":
            # Balance Calculation
            current_bal = state["balances"][self.human_agent.name]
            allocated = sum(self.current_allocations)
            remaining = current_bal - allocated

            # Instructions
            instr = self.font_s.render(
                "L-Click: +1 | R-Click: -1 | Shift: +/- 5", True, (150, 150, 150)
            )
            self.screen.blit(instr, (20, SCREEN_SIZE[1] - 40))

            # Remaining Troops Center Display
            rem_color = (100, 255, 100) if remaining >= 0 else (255, 50, 50)
            rem_txt = self.font_l.render(f"Remaining: {remaining}", True, rem_color)
            self.screen.blit(rem_txt, (SCREEN_SIZE[0] // 2 - 140, SCREEN_SIZE[1] - 180))

            # Submit Button
            btn_color = (
                (40, 100, 40) if remaining >= 0 else (60, 60, 60)
            )  # Dark green if valid, grey if not
            pygame.draw.rect(
                self.screen, btn_color, self.submit_btn_rect, border_radius=10
            )
            pygame.draw.rect(
                self.screen, (100, 200, 100), self.submit_btn_rect, 2, border_radius=10
            )

            btn_lbl = self.font_m.render("DEPLOY", True, (255, 255, 255))
            self.screen.blit(
                btn_lbl, btn_lbl.get_rect(center=self.submit_btn_rect.center)
            )

    def draw_game_over(self):
        overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        final_scores = self.env.get_state()["scores"]
        # final_scores = {"random_agent": 51, "uniform_agent": 122, "Your Agent": 122}
        max_score = max(final_scores.values())
        winners = [k for k in final_scores.keys() if final_scores.get(k) == max_score]
        if len(winners) > 1:
            txt = f"RESULT: Tie between {','.join(winners[:-1])} and {winners[-1]}"
        else:
            txt = f"WINNER: {winners[0]}"

        txt_win = self.font_xl.render(txt, True, ACCENT_COLOR)
        self.screen.blit(
            txt_win,
            txt_win.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 50)),
        )

        txt_sub = self.font_l.render(
            "Press ESC to Exit or ENTER to play again", True, TEXT_COLOR
        )
        self.screen.blit(
            txt_sub,
            txt_sub.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 50)),
        )

    def run(self):
        while True:
            self.handle_input()
            if self.state != "END":
                self.update()

            self.screen.fill(BG_COLOR)

            self.draw_battlefields()
            self.draw_hud()
            self.draw_troops_anim()
            self.draw_results_static()

            if self.state == "END":
                self.draw_game_over()
                # keys = pygame.key.get_pressed()
                pygame.display.update()
                pygame.event.clear()

                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.reset()
                        break
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

            elif self.state == "NEXT_ROUND":
                txt = self.font_m.render("Press ENTER to continue.", True, TEXT_COLOR)
                W, H = SCREEN_SIZE
                self.screen.blit(txt, txt.get_rect(center=(W // 2, H - 100)))
                pygame.display.update()
                pygame.event.clear()

                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        break

            pygame.display.flip()
            self.clock.tick(FPS)


class HumanPlaceholder(AbstractAgent):
    def get_allocation(self, *args, **kwargs):
        return []


if __name__ == "__main__":
    try:
        with open("./config.toml", "rb") as f:
            config = tomllib.load(f)
        num_fields = config["human_play"]["num_fields"]
        rounds = config["human_play"]["rounds"]
        start_balance = config["human_play"]["start_balance"]
    except Exception as e:
        print("Config not found or invalid, using defaults.")
        num_fields = 5
        rounds = 5
        start_balance = 100

    # Setup Env and Agents
    field_values = [np.random.randint(2, 10) for _ in range(num_fields)]

    human = HumanPlaceholder(name="You")

    # Load Opponents
    opponents = select_agents("Sample_Agents")
    for i, n in enumerate(opponents):
        n.name = f"Computer {i + 1}"
    if not opponents:
        print("No opponents found, please check agent path.")
        sys.exit()

    all_agent_names = [human.name] + [a.name for a in opponents]

    # Initialize Environment
    env = Env(
        agent_names=all_agent_names,
        field_values=field_values,
        num_fields=num_fields,
        total_rounds=rounds,
        starting_soldiers=start_balance,
    )

    # To - Do: check final winner calculations
    # update selecte agent function

    game = InteractiveGame(env, human, opponents)
    game.run()
