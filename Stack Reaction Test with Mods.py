import pygame
import random
import time
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No Spoilers")
FPS = 360

font = pygame.font.SysFont('timesnewroman.ttf', 36)
font2 = pygame.font.SysFont('timesnewroman.ttf', 72)

blue = (0, 0, 255)
black = (0, 0, 0)
pink = (255, 192, 203)


def circle(color, radii):
    pygame.draw.circle(screen, color, (WIDTH//2, HEIGHT//2), radii)


text = font.render("Press either mouse button, this is a reaction test. "
                   "Relax your hand and please prepare yourself to react!", False, (0, 255, 0))
text_2 = font2.render("Please read!", False, (0, 255, 0))
r_surf = None
ar_surf = None
r_surf_2 = None
ar_surf_2 = None

game_state = "start"
start_time = 0
average_time = 0

count = 0
end = False
running = True

Clock = pygame.time.Clock()

while running:

    Clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "start":
                game_state = "wait"
                start_time = current_time + random.uniform(2000, 5000)
            if game_state == "wait_for_reaction":
                game_state = "wait"
                reaction_time = (current_time - start_time) / 1000
                start_time = current_time + random.uniform(2000, 5000)
                count += 1
                average_time = (average_time * (count - 1) + reaction_time) / count
                r_surf = font.render(f"REACTION TIME: {reaction_time:.03f}s", False, (255, 255, 255))
                ar_surf = font.render(f"AVERAGE REACTION TIME IS: {average_time:.03f}s", False, (255, 255, 255))
            if game_state == "wait_for_reaction_2":
                game_state = "wait"
                reaction_time = (current_time - start_time) / 1000
                start_time = current_time + random.uniform(2000, 5000)
                count += 1
                average_time = (average_time * (count - 1) + reaction_time) / count
                r_surf_2 = font.render(f"'Just Do It' REACTION TIME: {reaction_time:.03f}s", False, (255, 255, 255))
                ar_surf_2 = font.render("Game is complete, please take note of your numbers and exit using "
                                        "task manager", False, (255, 255, 255))

    if game_state == "wait":
        while game_state == 'wait' and end is True:
            time.sleep(60)
        if current_time >= start_time:
            game_state = "wait_for_reaction"
            if count == 4:
                game_state = "wait_for_reaction_2"

    screen.fill(black)

    center = screen.get_rect().center

    if game_state == "start":
        screen.blit(text, text.get_rect(center=center))
        screen.blit(text_2, text_2.get_rect(center=(center[0], center[1]-HEIGHT//4)))
    if game_state == "wait_for_reaction":
        circle(blue, 20)
    if game_state == "wait_for_reaction_2":
        circle(pink, 2000)
    if r_surf:
        screen.blit(r_surf, r_surf.get_rect(center=(center[0], HEIGHT - 125)))
    if ar_surf:
        screen.blit(ar_surf, ar_surf.get_rect(center=(center[0], HEIGHT - 75)))
    if r_surf_2:
        screen.blit(r_surf_2, r_surf_2.get_rect(center=(center[0], HEIGHT - 25)))
    if ar_surf_2:
        screen.blit(ar_surf_2, ar_surf_2.get_rect(center=(center[0], center[1])))
        end = True

    pygame.display.flip()
