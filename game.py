import math
import random
import sys

import pygame

<<<<<<< HEAD
=======

# ----------------------------
# Configuration
# ----------------------------

>>>>>>> 1244f73 (second commit)
WIDTH, HEIGHT = 520, 760
FPS = 60

ROAD_LEFT, ROAD_RIGHT = 80, 440
LANE_CENTERS = [140, 260, 380]
PLAYER_Y = 620

PLAYER_WIDTH, PLAYER_HEIGHT = 42, 68
TRAFFIC_WIDTH, TRAFFIC_HEIGHT = 40, 62

INITIAL_SPEED = 245
MAX_SPEED = 470
INVULNERABILITY_TIME = 1.35

LANE_MARKER_SPACING = 82

WHITE = (238, 246, 255)
CYAN = (83, 242, 255)
PINK = (255, 66, 132)
YELLOW = (255, 218, 94)
DARK = (11, 17, 28)
ROAD = (35, 44, 55)


TRAFFIC_COLORS = [
    (255, 75, 107),
    (180, 111, 255),
    (255, 169, 70),
]


# ----------------------------
# Game
# ----------------------------

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Neon Rush — Hard Mode")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("consolas", 24, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 16)
        self.tiny_font = pygame.font.SysFont("consolas", 13)

        self.running = True
        self.touch_start = None
        self.start_button = None

        self.high_score = self.load_high_score()
        self.state = self.new_game()

    # ----------------------------
    # Persistence
    # ----------------------------

    @staticmethod
    def load_high_score():
        try:
            with open("highscore.txt", "r", encoding="utf-8") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        try:
            with open("highscore.txt", "w", encoding="utf-8") as file:
                file.write(str(self.high_score))
        except OSError:
            # The game should still work if saving is unavailable.
            pass

    # ----------------------------
    # State
    # ----------------------------

    @staticmethod
    def new_game():
        return {
            "player_lane": 1,
            "player_x": float(LANE_CENTERS[1]),
            "traffic": [],
            "coins": [],
            "spawn_timer": 0.45,
            "coin_timer": 1.8,
            "road_offset": 0.0,
            "score": 0,
            "score_float": 0.0,
            "coins_collected": 0,
            "lives": 3,
            "elapsed": 0.0,
            "invulnerable": 0.0,
            "game_over": False,
            "paused": False,
        }

    def reset(self):
        self.state = self.new_game()
        self.start_button = None
        self.touch_start = None

    # ----------------------------
    # Drawing helpers
    # ----------------------------

    @staticmethod
    def draw_text(surface, value, font, color, position, center=False):
        image = font.render(str(value), True, color)
        rect = image.get_rect()

        if center:
            rect.center = position
        else:
            rect.topleft = position

        surface.blit(image, rect)

    def draw_car(self, surface, x, y, color, player=False):
        width = PLAYER_WIDTH if player else TRAFFIC_WIDTH
        height = PLAYER_HEIGHT if player else TRAFFIC_HEIGHT

        rect = pygame.Rect(0, 0, width, height)
        rect.center = (int(x), int(y))

        # Shadow
        pygame.draw.rect(
            surface,
            (5, 8, 14),
            rect.inflate(8, 8),
            border_radius=10,
        )

        # Wheels
        for wheel_x in (rect.left - 3, rect.right - 2):
            pygame.draw.rect(
                surface,
                (8, 10, 15),
                (wheel_x, rect.top + 12, 6, 14),
                border_radius=2,
            )
            pygame.draw.rect(
                surface,
                (8, 10, 15),
                (wheel_x, rect.bottom - 25, 6, 14),
                border_radius=2,
            )

        # Body
        pygame.draw.rect(
            surface,
            color,
            rect,
            border_radius=9,
        )

        # Windshield
        glass = pygame.Rect(
            rect.left + 6,
            rect.top + 10,
            rect.width - 12,
            17,
        )

        pygame.draw.rect(
            surface,
            (20, 43, 60),
            glass,
            border_radius=5,
        )

        pygame.draw.line(
            surface,
            (112, 205, 228),
            glass.midleft,
            glass.midright,
            2,
        )

        # Rear window / center panel
        pygame.draw.rect(
            surface,
            (19, 34, 48),
            (rect.left + 7, rect.top + 34, rect.width - 14, 12),
            border_radius=3,
        )

        if player:
            # Headlights
            pygame.draw.rect(
                surface,
                (245, 255, 255),
                (rect.left + 5, rect.top + 3, 7, 5),
                border_radius=2,
            )
            pygame.draw.rect(
                surface,
                (245, 255, 255),
                (rect.right - 12, rect.top + 3, 7, 5),
                border_radius=2,
            )

            # Tail lights
            pygame.draw.rect(
                surface,
                PINK,
                (rect.left + 5, rect.bottom - 7, 8, 4),
                border_radius=2,
            )
            pygame.draw.rect(
                surface,
                PINK,
                (rect.right - 13, rect.bottom - 7, 8, 4),
                border_radius=2,
            )

            pygame.draw.rect(
                surface,
                WHITE,
                rect,
                2,
                border_radius=9,
            )
        else:
            pygame.draw.rect(
                surface,
                (255, 244, 205),
                (rect.left + 5, rect.bottom - 7, 8, 4),
                border_radius=2,
            )
            pygame.draw.rect(
                surface,
                (255, 244, 205),
                (rect.right - 13, rect.bottom - 7, 8, 4),
                border_radius=2,
            )

    def draw_coin(self, surface, x, y, pulse):
        radius = 12 + int(2 * math.sin(pulse))

        pygame.draw.circle(
            surface,
            (107, 78, 15),
            (int(x), int(y)),
            radius + 3,
        )
        pygame.draw.circle(
            surface,
            YELLOW,
            (int(x), int(y)),
            radius,
        )
        pygame.draw.circle(
            surface,
            (255, 247, 180),
            (int(x), int(y)),
            max(3, radius - 5),
            2,
        )

        self.draw_text(
            surface,
            "$",
            self.tiny_font,
            (112, 75, 9),
            (int(x), int(y) - 1),
            center=True,
        )

    # ----------------------------
    # Collision helpers
    # ----------------------------

    @staticmethod
    def car_rect(x, y, player=False):
        if player:
            width, height = 36, 58
        else:
            width, height = 34, 54

        return pygame.Rect(
            int(x - width / 2),
            int(y - height / 2),
            width,
            height,
        )

    @staticmethod
    def coin_rect(x, y):
        return pygame.Rect(
            int(x - 13),
            int(y - 13),
            26,
            26,
        )

    # ----------------------------
    # Spawning
    # ----------------------------

    def safe_spawn_lanes(self):
        blocked_lanes = {
            car["lane"]
            for car in self.state["traffic"]
            if car["y"] < 150
        }

        return [
            lane
            for lane in range(len(LANE_CENTERS))
            if lane not in blocked_lanes
        ]

    def spawn_traffic(self):
        safe_lanes = self.safe_spawn_lanes()

        if safe_lanes:
            lane = random.choice(safe_lanes)
        else:
            lane = random.randrange(len(LANE_CENTERS))

        self.state["traffic"].append(
            {
                "lane": lane,
                "y": -50.0,
                "color": random.choice(TRAFFIC_COLORS),
            }
        )

    def spawn_coin(self):
        lane = random.randrange(len(LANE_CENTERS))

        self.state["coins"].append(
            {
                "lane": lane,
                "y": -25.0,
                "phase": random.random() * math.tau,
            }
        )

    # ----------------------------
    # Game controls
    # ----------------------------

    def move_lane(self, direction):
        if self.state["game_over"] or self.state["paused"]:
            return

        current_lane = self.state["player_lane"]

        self.state["player_lane"] = max(
            0,
            min(len(LANE_CENTERS) - 1, current_lane + direction),
        )

    def toggle_pause(self):
        if not self.state["game_over"]:
            self.state["paused"] = not self.state["paused"]

    # ----------------------------
    # Game update
    # ----------------------------

    def current_speed(self):
        return min(
            MAX_SPEED,
            INITIAL_SPEED + self.state["elapsed"] * 4.8,
        )

    def update_score(self, dt):
        points_per_second = 12 + self.state["elapsed"] * 0.35

        self.state["score_float"] += points_per_second * dt
        self.state["score"] = int(self.state["score_float"])

        if self.state["score"] > self.high_score:
            self.high_score = self.state["score"]

    def finish_game(self):
        self.state["game_over"] = True
        self.save_high_score()

    def update(self, dt):
        if self.state["game_over"] or self.state["paused"]:
            return

        self.state["elapsed"] += dt
        self.update_score(dt)

        speed = self.current_speed()

        self.state["road_offset"] = (
            self.state["road_offset"] + speed * dt
        ) % LANE_MARKER_SPACING

        target_x = LANE_CENTERS[self.state["player_lane"]]

        self.state["player_x"] += (
            target_x - self.state["player_x"]
        ) * min(1.0, dt * 14)

        if self.state["invulnerable"] > 0:
            self.state["invulnerable"] -= dt

        # Traffic spawning
        self.state["spawn_timer"] -= dt

        spawn_interval = max(
            0.43,
            0.95 - self.state["elapsed"] * 0.006,
        )

        if self.state["spawn_timer"] <= 0:
            self.spawn_traffic()
            self.state["spawn_timer"] = (
                spawn_interval * random.uniform(0.72, 1.12)
            )

        # Coin spawning
        self.state["coin_timer"] -= dt

        if self.state["coin_timer"] <= 0:
            self.spawn_coin()
            self.state["coin_timer"] = random.uniform(1.2, 2.2)

        player_rect = self.car_rect(
            self.state["player_x"],
            PLAYER_Y,
            player=True,
        )

        # Traffic update and collision
        for car in self.state["traffic"][:]:
            car["y"] += speed * dt

            if car["y"] > HEIGHT + 70:
                self.state["traffic"].remove(car)
                self.state["score_float"] += 20
                self.state["score"] = int(self.state["score_float"])
                continue

            traffic_rect = self.car_rect(
                LANE_CENTERS[car["lane"]],
                car["y"],
            )

            if (
                self.state["invulnerable"] <= 0
                and player_rect.colliderect(traffic_rect)
            ):
                self.state["traffic"].remove(car)
                self.state["lives"] -= 1
                self.state["invulnerable"] = INVULNERABILITY_TIME

                if self.state["lives"] <= 0:
                    self.finish_game()

        # Coin update and collection
        for coin in self.state["coins"][:]:
            coin["y"] += speed * dt

            if coin["y"] > HEIGHT + 30:
                self.state["coins"].remove(coin)
                continue

            coin_collision = self.coin_rect(
                LANE_CENTERS[coin["lane"]],
                coin["y"],
            )

            if player_rect.colliderect(coin_collision):
                self.state["coins"].remove(coin)
                self.state["coins_collected"] += 1
                self.state["score_float"] += 100
                self.state["score"] = int(self.state["score_float"])

    def draw_scene(self):
        state = self.state

        self.screen.fill(DARK)

        # Background stars
        for index in range(45):
            x = (index * 73 + 19) % WIDTH
            y = (
                index * 97
                + int(state["elapsed"] * 16)
            ) % HEIGHT

            pygame.draw.circle(
                self.screen,
                (47, 77, 91),
                (x, y),
                1,
            )

        # Roadside areas
        pygame.draw.rect(
            self.screen,
            (17, 31, 34),
            (0, 0, ROAD_LEFT, HEIGHT),
        )
        pygame.draw.rect(
            self.screen,
            (17, 31, 34),
            (ROAD_RIGHT, 0, WIDTH - ROAD_RIGHT, HEIGHT),
        )

        # Road
        pygame.draw.rect(
            self.screen,
            ROAD,
            (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT),
        )

        # Road borders
        pygame.draw.line(
            self.screen,
            CYAN,
            (ROAD_LEFT, 0),
            (ROAD_LEFT, HEIGHT),
            3,
        )
        pygame.draw.line(
            self.screen,
            PINK,
            (ROAD_RIGHT, 0),
            (ROAD_RIGHT, HEIGHT),
            3,
        )

        # Dashed lane markers
        for lane_marker_x in (200, 320):
            for index in range(12):
                y = (
                    index * LANE_MARKER_SPACING
                    + state["road_offset"]
                ) % (HEIGHT + LANE_MARKER_SPACING) - LANE_MARKER_SPACING

                pygame.draw.rect(
                    self.screen,
                    (178, 197, 208),
                    (lane_marker_x - 2, y, 4, 43),
                    border_radius=2,
                )

        # Roadside reflectors
        for index in range(14):
            y = (
                index * 65
                + state["road_offset"] * 1.25
            ) % (HEIGHT + 65) - 65

            pygame.draw.rect(
                self.screen,
                (255, 60, 123),
                (ROAD_LEFT - 10, y, 5, 17),
                border_radius=2,
            )
            pygame.draw.rect(
                self.screen,
                (77, 228, 255),
                (ROAD_RIGHT + 5, y, 5, 17),
                border_radius=2,
            )

        # Coins
        for coin in state["coins"]:
            self.draw_coin(
                self.screen,
                LANE_CENTERS[coin["lane"]],
                coin["y"],
                state["elapsed"] * 8 + coin["phase"],
            )

        # Traffic
        for car in state["traffic"]:
            self.draw_car(
                self.screen,
                LANE_CENTERS[car["lane"]],
                car["y"],
                car["color"],
            )

        # Player
        should_draw_player = (
            state["invulnerable"] <= 0
            or int(state["elapsed"] * 12) % 2 == 0
        )

        if should_draw_player:
            self.draw_car(
                self.screen,
                state["player_x"],
                PLAYER_Y,
                (30, 145, 255),
                player=True,
            )

        # HUD
        pygame.draw.rect(
            self.screen,
            (8, 13, 24),
            (12, 12, WIDTH - 24, 82),
            border_radius=12,
        )

        pygame.draw.rect(
            self.screen,
            (57, 87, 109),
            (12, 12, WIDTH - 24, 82),
            1,
            border_radius=12,
        )

        self.draw_text(
            self.screen,
            "NEON RUSH",
            self.small_font,
            CYAN,
            (25, 20),
        )
        self.draw_text(
            self.screen,
            f"SCORE {state['score']:06d}",
            self.small_font,
            WHITE,
            (25, 45),
        )
        self.draw_text(
            self.screen,
            f"COINS {state['coins_collected']:02d}",
            self.small_font,
            YELLOW,
            (230, 45),
        )
        self.draw_text(
            self.screen,
            f"LIVES {'♥' * state['lives']}",
            self.small_font,
            PINK,
            (390, 45),
        )

        speed_display = int(160 + state["elapsed"] * 3.2)

        self.draw_text(
            self.screen,
            f"{speed_display} KM/H",
            self.tiny_font,
            (172, 220, 230),
            (WIDTH - 26, 20),
        )

        self.draw_text(
            self.screen,
            "← / → or A / D to steer     P: pause",
            self.tiny_font,
            (183, 205, 215),
            (WIDTH // 2, HEIGHT - 15),
            center=True,
        )

    def draw_overlay(self, title, subtitle, lines, button_label):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((3, 7, 15, 185))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(42, 220, WIDTH - 84, 310)

        pygame.draw.rect(
            self.screen,
            (12, 23, 38),
            panel,
            border_radius=18,
        )
        pygame.draw.rect(
            self.screen,
            CYAN,
            panel,
            2,
            border_radius=18,
        )

        self.draw_text(
            self.screen,
            title,
            self.font,
            CYAN,
            (WIDTH // 2, 265),
            center=True,
        )

        self.draw_text(
            self.screen,
            subtitle,
            self.small_font,
            WHITE,
            (WIDTH // 2, 305),
            center=True,
        )

        for index, line in enumerate(lines):
            self.draw_text(
                self.screen,
                line,
                self.small_font,
                (210, 229, 239),
                (WIDTH // 2, 350 + index * 28),
                center=True,
            )

        button = pygame.Rect(105, 445, 310, 48)

        pygame.draw.rect(
            self.screen,
            (30, 117, 155),
            button,
            border_radius=10,
        )
        pygame.draw.rect(
            self.screen,
            (138, 246, 255),
            button,
            2,
            border_radius=10,
        )

        self.draw_text(
            self.screen,
            button_label,
            self.small_font,
            WHITE,
            button.center,
            center=True,
        )

        self.draw_text(
            self.screen,
            "ESC to quit",
            self.tiny_font,
            (150, 174, 190),
            (WIDTH // 2, 505),
            center=True,
        )

        return button

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.move_lane(-1)

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.move_lane(1)

            elif event.key == pygame.K_p:
                self.toggle_pause()

            elif event.key == pygame.K_r:
                self.reset()

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.state["game_over"]:
                    self.reset()
                elif self.state["paused"]:
                    self.state["paused"] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                return

            self.touch_start = event.pos

            if self.state["game_over"]:
                if (
                    self.start_button
                    and self.start_button.collidepoint(event.pos)
                ):
                    self.reset()

            elif self.state["paused"]:
                if (
                    self.start_button
                    and self.start_button.collidepoint(event.pos)
                ):
                    self.state["paused"] = False

            else:
                # Tap left or right side of the screen to change lanes.
                if event.pos[0] < WIDTH / 2:
                    self.move_lane(-1)
                else:
                    self.move_lane(1)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button != 1:
                return

            if self.touch_start is not None:
                dx = event.pos[0] - self.touch_start[0]

                if (
                    not self.state["game_over"]
                    and not self.state["paused"]
                    and abs(dx) >= 40
                ):
                    self.move_lane(1 if dx > 0 else -1)

            self.touch_start = None


    def run(self):
        while self.running:
            dt = min(
                self.clock.tick(FPS) / 1000.0,
                0.04,
            )

            for event in pygame.event.get():
                self.handle_event(event)

            self.update(dt)
            self.draw_scene()

            if self.state["game_over"]:
                self.start_button = self.draw_overlay(
                    "RACE OVER",
                    f"FINAL SCORE: {self.state['score']}",
                    [
                        f"Coins collected: {self.state['coins_collected']}",
                        f"Survival time: {int(self.state['elapsed'])} seconds",
                        f"Best score: {self.high_score}",
                        "Dodge traffic and grab coins to score!",
                    ],
                    "START / RESTART  [ENTER]",
                )

            elif self.state["paused"]:
                self.start_button = self.draw_overlay(
                    "PAUSED",
                    f"SCORE: {self.state['score']}",
                    [
                        "Press P or ENTER to continue",
                        "Use left/right arrows or A/D",
                        "R restarts the current game",
                    ],
                    "RESUME  [ENTER]",
                )

            elif self.state["elapsed"] < 2.4:
                self.draw_text(
                    self.screen,
                    "HARD MODE: THREE LIVES. GOOD LUCK!",
                    self.tiny_font,
                    YELLOW,
                    (WIDTH // 2, 120),
                    center=True,
                )

            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()