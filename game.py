import math
import random
import sys
import pygame

WIDTH, HEIGHT = 520, 760
FPS = 60
ROAD_LEFT, ROAD_RIGHT = 80, 440
LANE_CENTERS = [140, 260, 380]
PLAYER_Y = 620
WHITE = (238, 246, 255)
CYAN = (83, 242, 255)
PINK = (255, 66, 132)
YELLOW = (255, 218, 94)
DARK = (11, 17, 28)
ROAD = (35, 44, 55)

pygame.init()
pygame.display.set_caption("Neon Rush — Hard Mode")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24, bold=True)
small = pygame.font.SysFont("consolas", 16)
tiny = pygame.font.SysFont("consolas", 13)

def text(surface, value, font_obj, color, pos, center=False):
    image = font_obj.render(str(value), True, color)
    rect = image.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(image, rect)

def draw_car(surface, x, y, color, player=False):
    rect = pygame.Rect(0, 0, 42 if player else 40, 68 if player else 62)
    rect.center = (int(x), int(y))
    # shadow and wheels
    pygame.draw.rect(surface, (5, 8, 14), rect.inflate(8, 8), border_radius=10)
    for wx in (rect.left - 3, rect.right - 2):
        pygame.draw.rect(surface, (8, 10, 15), (wx, rect.top + 12, 6, 14), border_radius=2)
        pygame.draw.rect(surface, (8, 10, 15), (wx, rect.bottom - 25, 6, 14), border_radius=2)
    pygame.draw.rect(surface, color, rect, border_radius=9)
    # windshield
    glass = pygame.Rect(rect.left + 6, rect.top + 10, rect.width - 12, 17)
    pygame.draw.rect(surface, (20, 43, 60), glass, border_radius=5)
    pygame.draw.line(surface, (112, 205, 228), glass.midleft, glass.midright, 2)
    pygame.draw.rect(surface, (19, 34, 48), (rect.left + 7, rect.top + 34, rect.width - 14, 12), border_radius=3)
    if player:
        pygame.draw.rect(surface, (245, 255, 255), (rect.left + 5, rect.top + 3, 7, 5), border_radius=2)
        pygame.draw.rect(surface, (245, 255, 255), (rect.right - 12, rect.top + 3, 7, 5), border_radius=2)
        pygame.draw.rect(surface, PINK, (rect.left + 5, rect.bottom - 7, 8, 4), border_radius=2)
        pygame.draw.rect(surface, PINK, (rect.right - 13, rect.bottom - 7, 8, 4), border_radius=2)
        pygame.draw.rect(surface, WHITE, rect, 2, border_radius=9)
    else:
        pygame.draw.rect(surface, (255, 244, 205), (rect.left + 5, rect.bottom - 7, 8, 4), border_radius=2)
        pygame.draw.rect(surface, (255, 244, 205), (rect.right - 13, rect.bottom - 7, 8, 4), border_radius=2)

def draw_coin(surface, x, y, pulse):
    r = 12 + int(2 * math.sin(pulse))
    pygame.draw.circle(surface, (107, 78, 15), (int(x), int(y)), r + 3)
    pygame.draw.circle(surface, YELLOW, (int(x), int(y)), r)
    pygame.draw.circle(surface, (255, 247, 180), (int(x), int(y)), max(3, r - 5), 2)
    text(surface, "$", tiny, (112, 75, 9), (int(x), int(y) - 1), center=True)

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
        "coins_collected": 0,
        "lives": 3,
        "elapsed": 0.0,
        "invulnerable": 0.0,
        "game_over": False,
        "paused": False,
    }

state = new_game()

def spawn_traffic():
    lane = random.randrange(3)
    # Avoid creating a near-immediate unavoidable wall of traffic.
    if state["traffic"] and all(abs(t["y"] - 90) < 100 and t["lane"] != lane for t in state["traffic"]):
        lane = random.choice([i for i in range(3) if i not in [t["lane"] for t in state["traffic"] if t["y"] < 180]] or [lane])
    state["traffic"].append({"lane": lane, "y": -50.0, "color": random.choice([(255, 75, 107), (180, 111, 255), (255, 169, 70)])})

def spawn_coin():
    lane = random.randrange(3)
    state["coins"].append({"lane": lane, "y": -25.0, "phase": random.random() * 6})

def rect_for_car(x, y, player=False):
    w, h = (34, 56) if player else (32, 52)
    return pygame.Rect(int(x - w / 2), int(y - h / 2), w, h)

def draw_scene():
    screen.fill(DARK)
    # distant neon stars
    for i in range(45):
        x = (i * 73 + 19) % WIDTH
        y = (i * 97 + int(state["elapsed"] * 16)) % HEIGHT
        pygame.draw.circle(screen, (47, 77, 91), (x, y), 1)
    pygame.draw.rect(screen, (17, 31, 34), (0, 0, ROAD_LEFT, HEIGHT))
    pygame.draw.rect(screen, (17, 31, 34), (ROAD_RIGHT, 0, WIDTH - ROAD_RIGHT, HEIGHT))
    pygame.draw.rect(screen, ROAD, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
    pygame.draw.line(screen, CYAN, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 3)
    pygame.draw.line(screen, PINK, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 3)
    # dashed lane markers
    for x in (200, 320):
        for i in range(12):
            y = (i * 82 + state["road_offset"]) % (HEIGHT + 82) - 82
            pygame.draw.rect(screen, (178, 197, 208), (x - 2, y, 4, 43), border_radius=2)
    # roadside reflectors
    for i in range(14):
        y = (i * 65 + state["road_offset"] * 1.25) % (HEIGHT + 65) - 65
        pygame.draw.rect(screen, (255, 60, 123), (ROAD_LEFT - 10, y, 5, 17), border_radius=2)
        pygame.draw.rect(screen, (77, 228, 255), (ROAD_RIGHT + 5, y, 5, 17), border_radius=2)

    for coin in state["coins"]:
        draw_coin(screen, LANE_CENTERS[coin["lane"]], coin["y"], state["elapsed"] * 8 + coin["phase"])
    for car in state["traffic"]:
        draw_car(screen, LANE_CENTERS[car["lane"]], car["y"], car["color"])
    if state["invulnerable"] <= 0 or int(state["elapsed"] * 12) % 2 == 0:
        draw_car(screen, state["player_x"], PLAYER_Y, (30, 145, 255), True)

    # HUD
    pygame.draw.rect(screen, (8, 13, 24), (12, 12, WIDTH - 24, 82), border_radius=12)
    pygame.draw.rect(screen, (57, 87, 109), (12, 12, WIDTH - 24, 82), 1, border_radius=12)
    text(screen, "NEON RUSH", small, CYAN, (25, 20))
    text(screen, f"SCORE {state['score']:06d}", small, WHITE, (25, 45))
    text(screen, f"COINS {state['coins_collected']:02d}", small, YELLOW, (230, 45))
    text(screen, f"LIVES {'♥' * state['lives']}", small, PINK, (390, 45))
    speed = int(160 + state["elapsed"] * 3.2)
    text(screen, f"{speed} KM/H", tiny, (172, 220, 230), (WIDTH - 26, 20), center=False)
    # bottom controls hint
    text(screen, "← / → or A / D to steer     P: pause", tiny, (183, 205, 215), (WIDTH // 2, HEIGHT - 15), center=True)

def draw_overlay(title, subtitle, lines):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((3, 7, 15, 185))
    screen.blit(overlay, (0, 0))
    panel = pygame.Rect(42, 220, WIDTH - 84, 310)
    pygame.draw.rect(screen, (12, 23, 38), panel, border_radius=18)
    pygame.draw.rect(screen, CYAN, panel, 2, border_radius=18)
    text(screen, title, font, CYAN, (WIDTH // 2, 265), center=True)
    text(screen, subtitle, small, WHITE, (WIDTH // 2, 305), center=True)
    for i, line in enumerate(lines):
        text(screen, line, small, (210, 229, 239), (WIDTH // 2, 350 + i * 28), center=True)
    button = pygame.Rect(105, 445, 310, 48)
    pygame.draw.rect(screen, (30, 117, 155), button, border_radius=10)
    pygame.draw.rect(screen, (138, 246, 255), button, 2, border_radius=10)
    text(screen, "START / RESTART  [ENTER]", small, WHITE, button.center, center=True)
    text(screen, "ESC to quit", tiny, (150, 174, 190), (WIDTH // 2, 505), center=True)
    return button

def move_lane(direction):
    if not state["game_over"] and not state["paused"]:
        state["player_lane"] = max(0, min(2, state["player_lane"] + direction))

def update(dt):
    if state["game_over"] or state["paused"]:
        return
    state["elapsed"] += dt
    state["score"] += int(dt * (12 + state["elapsed"] * 0.35))
    speed = min(470, 245 + state["elapsed"] * 4.8)
    state["road_offset"] = (state["road_offset"] + speed * dt) % 82
    state["player_x"] += (LANE_CENTERS[state["player_lane"]] - state["player_x"]) * min(1, dt * 14)
    if state["invulnerable"] > 0:
        state["invulnerable"] -= dt

    state["spawn_timer"] -= dt
    spawn_interval = max(0.43, 0.95 - state["elapsed"] * 0.006)
    if state["spawn_timer"] <= 0:
        spawn_traffic()
        state["spawn_timer"] = spawn_interval * random.uniform(0.72, 1.12)

    state["coin_timer"] -= dt
    if state["coin_timer"] <= 0:
        spawn_coin()
        state["coin_timer"] = random.uniform(1.2, 2.2)

    player_rect = rect_for_car(state["player_x"], PLAYER_Y, True)
    for car in state["traffic"][:]:
        car["y"] += speed * dt
        if car["y"] > HEIGHT + 70:
            state["traffic"].remove(car)
            state["score"] += 20
            continue
        if state["invulnerable"] <= 0 and player_rect.colliderect(rect_for_car(LANE_CENTERS[car["lane"]], car["y"])):
            state["traffic"].remove(car)
            state["lives"] -= 1
            state["invulnerable"] = 1.35
            if state["lives"] <= 0:
                state["game_over"] = True

    for coin in state["coins"][:]:
        coin["y"] += speed * dt
        if coin["y"] > HEIGHT + 30:
            state["coins"].remove(coin)
            continue
        coin_rect = pygame.Rect(LANE_CENTERS[coin["lane"]] - 13, int(coin["y"]) - 13, 26, 26)
        if player_rect.colliderect(coin_rect):
            state["coins"].remove(coin)
            state["coins_collected"] += 1
            state["score"] += 100

def main():
    global state
    running = True
    start_button = None
    touch_start = None
    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.04)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    move_lane(-1)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    move_lane(1)
                elif event.key == pygame.K_p and not state["game_over"]:
                    state["paused"] = not state["paused"]
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE) and (state["game_over"] or state["paused"]):
                    state = new_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    touch_start = event.pos
                    if (state["game_over"] or state["paused"]) and start_button and start_button.collidepoint(event.pos):
                        state = new_game()
                    elif not state["game_over"] and not state["paused"]:
                        if event.pos[0] < WIDTH / 2:
                            move_lane(-1)
                        else:
                            move_lane(1)
            elif event.type == pygame.MOUSEBUTTONUP:
                touch_start = None

        update(dt)
        draw_scene()
        if state["game_over"]:
            start_button = draw_overlay("RACE OVER", f"FINAL SCORE: {state['score']}", [
                f"Coins collected: {state['coins_collected']}",
                f"Survival time: {int(state['elapsed'])} seconds",
                "Dodge traffic and grab coins to score!"
            ])
        elif state["paused"]:
            start_button = draw_overlay("PAUSED", f"SCORE: {state['score']}", [
                "Press P to continue",
                "Use left/right arrows or A/D",
                "Avoid traffic; each crash costs a life"
            ])
        elif state["elapsed"] < 2.4:
            # brief start hint
            text(screen, "HARD MODE: THREE LIVES. GOOD LUCK!", tiny, YELLOW, (WIDTH // 2, 120), center=True)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
