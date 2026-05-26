import pygame
import random
import os

# =========================
# INITIALIZATION
# =========================

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No Spoilers")

CLOCK = pygame.time.Clock()
FPS = 1040

# =========================
# COLORS
# =========================

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# =========================
# FONTS
# =========================

FONT = pygame.font.SysFont("Segoe UI", 36)
BIG_FONT = pygame.font.SysFont("Segoe UI", 72)

# =========================
# GAME STATES
# =========================

START = "start"
WAITING = "waiting"
REACT = "react"
FALSE_START = "false_start"
FINAL_REACT = "final_react"
FINISHED = "finished"

# =========================
# HELPER FUNCTIONS
# =========================


def draw_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, text_surface.get_rect(center=position))


def draw_circle(color, radius):
    pygame.draw.circle(screen, color, (WIDTH // 2, HEIGHT // 2), radius)


def get_random_delay(start, finish):
    return random.uniform(start, finish)


def calculate_average(current_average, tally, new_time):
    return (current_average * (tally - 1) + new_time) / tally


# =========================
# GAME VARIABLES
# =========================

running = True
game_state = START

start_time = 0

reaction_time = 0
average_time = 0

count = 0

# =========================
# MAIN LOOP
# =========================

while running:

    CLOCK.tick(FPS)

    current_time = pygame.time.get_ticks()

    # =====================
    # EVENT HANDLING
    # =====================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_q:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_state == START:
                game_state = WAITING
                start_time = current_time + get_random_delay(2000, 5000)

            elif game_state == WAITING:
                start_time = current_time + get_random_delay(2000, 5000)
                game_state = FALSE_START

            elif game_state == FALSE_START:
                game_state = WAITING
                start_time = current_time + get_random_delay(2000, 5000)

            elif game_state in [REACT, FINAL_REACT]:

                reaction_time = (current_time - start_time) / 1000

                count += 1

                average_time = calculate_average(
                    average_time,
                    count,
                    reaction_time
                )

                if game_state == FINAL_REACT:
                    game_state = FINISHED

                else:
                    game_state = WAITING
                    start_time = current_time + get_random_delay(2000, 5000)

    # =====================
    # GAME LOGIC
    # =====================

    if game_state == WAITING:

        if current_time >= start_time:

            if count >= 4:
                game_state = FINAL_REACT
            else:
                game_state = REACT

    # =====================
    # DRAWING
    # =====================

    screen.fill(BLACK)

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    if game_state == START:

        draw_text(
            screen,
            "Please read!",
            BIG_FONT,
            GREEN,
            (center_x, center_y - HEIGHT // 4)
        )

        draw_text(
            screen,
            "Press either mouse button. Relax and prepare to react.",
            FONT,
            GREEN,
            (center_x, center_y)
        )

    elif game_state == FALSE_START:
        draw_text(
            screen,
            "You have pressed the mouse button too early. Please prepare, then press the mouse button again.",
            FONT,
            GREEN,
            (center_x, center_y)
        )

    elif game_state == WAITING:
        draw_text(
            screen,
            "",
            FONT,
            GREEN,
            (center_x, center_y)
        )

    elif game_state == REACT:

        draw_circle(BLUE, 20)

    elif game_state == FINAL_REACT:

        draw_circle(PINK, 2000)

    elif game_state == FINISHED:

        draw_text(
            screen,
            f"FINAL REACTION TIME: {reaction_time:.03f}s",
            FONT,
            WHITE,
            (center_x, center_y - 60)
        )

        draw_text(
            screen,
            f"AVERAGE REACTION TIME: {average_time:.03f}s",
            FONT,
            WHITE,
            (center_x, center_y)
        )

        draw_text(
            screen,
            "Press ESC or Q to quit.",
            FONT,
            WHITE,
            (center_x, center_y + 60)
        )

    # Persistent stats display
    if count > 0 and game_state != FINISHED:

        draw_text(
            screen,
            f"REACTION TIME: {reaction_time:.03f}s",
            FONT,
            WHITE,
            (center_x, HEIGHT - 125)
        )

        draw_text(
            screen,
            f"AVERAGE REACTION TIME: {average_time:.03f}s",
            FONT,
            WHITE,
            (center_x, HEIGHT - 75)
        )

    pygame.display.flip()

# =========================
# CLEAN EXIT
# =========================

pygame.quit()
