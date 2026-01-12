import random
import pygame
import math
import sys

pygame.init()
pygame.mixer.init()

# Настройки
gravity = 0.5
jump_strength = -10
velocity = 0
y = 100
points = 0

# Позиции труб
pomeha_x1 = 1400
pomeha_y1 = random.randint(400, 700)
pomeha_x2 = 2100
pomeha_y2 = random.randint(400, 700)

# Спрайты
sprite_city = pygame.image.load("background_city.png")
sprite_city = pygame.transform.scale(sprite_city, (1360, 768))
sprite_player = pygame.image.load("flappy.png")
sprite_pomeha1 = pygame.image.load("pipee.png")
sprite_pomeha2 = pygame.image.load("pipe.png")
sprite_boss = pygame.transform.scale(pygame.image.load("boss.png"), (350, 350))

sprite_projectile = pygame.Surface((30, 30))
sprite_projectile.fill((255, 0, 0))

# Звук
hit_sound = pygame.mixer.Sound('flappy-bird-hit.mp3')
loose_sound = pygame.mixer.Sound('die.mp3')
sound = pygame.mixer.Sound('flap.mp3')
point_sound = pygame.mixer.Sound('point.mp3')
swoosh_sound = pygame.mixer.Sound("swoosh.mp3")
for s in [hit_sound, loose_sound, sound, point_sound, swoosh_sound]:
    s.set_volume(0.2)
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)
swoosh_sound.play()

# Экран
screen = pygame.display.set_mode((1360, 768))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Босс
boss_x, boss_y = 900, 300
boss_direction = 2
boss_projectiles = []
last_projectile_time = 0

def spawn_boss(player_y, player_rect):
    global boss_y, boss_direction, last_projectile_time, boss_projectiles, points

    current_time = pygame.time.get_ticks()
    boss_y += boss_direction
    if boss_y <= 50 or boss_y >= 400:
        boss_direction *= -1

    screen.blit(sprite_boss, (boss_x, boss_y))

    if current_time - last_projectile_time > 2000:
        last_projectile_time = current_time
        dx = 100 - boss_x
        dy = player_y - boss_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx /= distance
        dy /= distance
        velocity_proj = 8
        proj_x = boss_x + 60
        proj_y = boss_y + 60
        boss_projectiles.append({
            "rect": pygame.Rect(proj_x, proj_y, 30, 30),
            "velocity": (dx * velocity_proj, dy * velocity_proj)
        })

    for proj in boss_projectiles[:]:
        proj["rect"].x += proj["velocity"][0]
        proj["rect"].y += proj["velocity"][1]
        screen.blit(sprite_projectile, proj["rect"])

        if proj["rect"].colliderect(player_rect):
            hit_sound.play()
            pygame.mixer.music.stop()
            pygame.time.delay(500)
            show_game_over()

        if proj["rect"].x < 0 or proj["rect"].y < 0 or proj["rect"].y > 768:
            boss_projectiles.remove(proj)
            points += 1

def show_game_over():
    font = pygame.font.Font('freesansbold.ttf', 64)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (screen.get_width() // 2 - 180, screen.get_height() // 2 - 120))

    btn_font = pygame.font.Font('freesansbold.ttf', 32)

    exit_text = btn_font.render("Выход", True, (255, 255, 255))
    exit_rect = pygame.Rect(screen.get_width() // 2 - 180, screen.get_height() // 2, 160, 60)
    pygame.draw.rect(screen, (0, 0, 0), exit_rect, border_radius=10)
    screen.blit(exit_text, (exit_rect.x + 30, exit_rect.y + 15))

    restart_text = btn_font.render("Рестарт", True, (255, 255, 255))
    restart_rect = pygame.Rect(screen.get_width() // 2 + 20, screen.get_height() // 2, 160, 60)
    pygame.draw.rect(screen, (0, 0, 0), restart_rect, border_radius=10)
    screen.blit(restart_text, (restart_rect.x + 25, restart_rect.y + 15))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if restart_rect.collidepoint(event.pos):
                    main()

def show_start_menu():
    btn_font = pygame.font.Font('freesansbold.ttf', 60)
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    hint_font = pygame.font.Font('freesansbold.ttf', 28)

    button_text = btn_font.render("Начать игру", True, (255, 255, 255))
    button_rect = pygame.Rect(screen.get_width() // 2 - 200, screen.get_height() // 2, 400, 90)

    title_text = title_font.render("FLAPPY BIRD", True, (255, 215, 0))
    title_pos = (screen.get_width() // 2 - title_text.get_width() // 2, screen.get_height() // 3 - 100)

    running_menu = True
    while running_menu:
        screen.fill((30, 144, 255))  # насыщенный синий фон
        screen.blit(sprite_city, (0, 0))

        screen.blit(title_text, title_pos)

        mouse_pos = pygame.mouse.get_pos()

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 140, 0), button_rect, border_radius=15)
        else:
            pygame.draw.rect(screen, (255, 69, 0), button_rect, border_radius=15)

        screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                                  button_rect.y + (button_rect.height - button_text.get_height()) // 2))

        hint = "Нажмите пробел или клик мыши, чтобы прыгать"
        hint_shadow = hint_font.render(hint, True, (0, 0, 0))
        hint_text = hint_font.render(hint, True, (255, 255, 255))
        hint_pos = (screen.get_width() // 2 - hint_text.get_width() // 2, button_rect.y + button_rect.height + 30)
        screen.blit(hint_shadow, (hint_pos[0] + 2, hint_pos[1] + 2))
        screen.blit(hint_text, hint_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    running_menu = False

        pygame.display.update()
        clock.tick(60)

def draw_score(points):
    font = pygame.font.Font('freesansbold.ttf', 72)
    text = str(points)
    # Рисуем обводку (чёрную) для цифр
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,2),(-2,2),(2,-2)]:
        outline = font.render(text, True, (0, 0, 0))
        screen.blit(outline, (screen.get_width()//2 - outline.get_width()//2 + dx, 50 + dy))
    # Рисуем сами цифры белым
    score_text = font.render(text, True, (255, 255, 255))
    screen.blit(score_text, (screen.get_width()//2 - score_text.get_width()//2, 50))

def main():
    global y, velocity, points, pomeha_x1, pomeha_y1, pomeha_x2, pomeha_y2, boss_projectiles, boss_y, boss_direction
    y = 100
    velocity = 0
    points = 0
    pomeha_x1 = 1400
    pomeha_y1 = random.randint(400, 700)
    pomeha_x2 = 2100
    pomeha_y2 = random.randint(400, 700)
    boss_projectiles = []
    boss_y = 300
    boss_direction = 2

    while True:
        screen.fill((100, 200, 255))
        screen.blit(sprite_city, (0, 0))

        boss_active = 20 <= points < 30

        angle = max(-30, min(velocity * -3, 30))
        rotated_player = pygame.transform.rotate(pygame.transform.scale(sprite_player, (120, 80)), angle)
        player_rect = rotated_player.get_rect(center=(100 + 60, y + 40))
        screen.blit(rotated_player, player_rect.topleft)

        if not boss_active:
            pomeha_x1 -= 15
            pomeha_x2 -= 15

            if pomeha_x1 <= 100:
                point_sound.play()
                pomeha_x1 = 1400
                pomeha_y1 = random.randint(400, 700)
                points += 1

            if pomeha_x2 <= 100:
                point_sound.play()
                pomeha_x2 = 1400
                pomeha_y2 = random.randint(400, 700)
                points += 1

            screen.blit(pygame.transform.scale(sprite_pomeha1, (80, 400)), (pomeha_x1, pomeha_y1))
            screen.blit(pygame.transform.scale(sprite_pomeha2, (80, 400)), (pomeha_x1, pomeha_y1 - 700))
            screen.blit(pygame.transform.scale(sprite_pomeha1, (80, 400)), (pomeha_x2, pomeha_y2))
            screen.blit(pygame.transform.scale(sprite_pomeha2, (80, 400)), (pomeha_x2, pomeha_y2 - 700))

            pipes = [
                pygame.Rect(pomeha_x1, pomeha_y1, 80, 400),
                pygame.Rect(pomeha_x1, pomeha_y1 - 700, 80, 400),
                pygame.Rect(pomeha_x2, pomeha_y2, 80, 400),
                pygame.Rect(pomeha_x2, pomeha_y2 - 700, 80, 400)
            ]

            for pipe in pipes:
                if player_rect.colliderect(pipe):
                    hit_sound.play()
                    pygame.mixer.music.stop()
                    pygame.time.delay(500)
                    show_game_over()

        else:
            spawn_boss(y, player_rect)

        velocity += gravity

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # --- Управление: добавлен клик мыши ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                velocity = jump_strength
                sound.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity = jump_strength
                    sound.play()

        y += velocity

        if y > 768 or y < -100:
            loose_sound.play()
            pygame.mixer.music.stop()
            pygame.time.delay(500)
            show_game_over()

        draw_score(points)  # Используем новую функцию с цифрами по центру

        pygame.display.update()
        clock.tick(60)

show_start_menu()
main()


