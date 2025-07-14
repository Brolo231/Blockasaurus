import sys
import random
import asyncio
import pygame

# -------------------- CONSTANTS --------------------

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (45, 45, 45)
LIGHT_GREY = (25, 25, 25)

PLAYER_SIZE = 75
PLAYER_X_CORD = PLAYER_SIZE

FLOOR = SCREEN_HEIGHT - PLAYER_SIZE * 2

TREE_WIDTH = 25
TREE_HEIGHT = 50
BIRD_WIDTH = 100
BIRD_HEIGHT = 25

JUMP_HEIGHT = 200
SLOW_DOWN_HEIGHT = 75

game_state = "menu"
restart = False
counter = 0
high_score = 0


# -------------------- TEXT FUNCTION --------------------

def draw_text(surface, text, font_size, color, position, center=True):
    font = pygame.font.SysFont("Arial", font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position if center else position)
    surface.blit(text_surface, text_rect)


# -------------------- PLAYER --------------------

class Player:
    def __init__(self):
        self.player = pygame.Rect(PLAYER_X_CORD, FLOOR, PLAYER_SIZE, PLAYER_SIZE)
        self.is_jumping = False
        self.is_falling = False
        self.slow_down = False
        self.gravity = 0.5
        self.velocity = 0.40
        self.health = 3
        self.mouse_pos = None

    def update(self, objects, delta_time, **kwargs):
        global counter, game_state, high_score, restart

        # Adjust speed based on score
        # Adjust velocity based on score
        if counter <= 5:
            self.velocity = 0.40
        elif 5 < counter <= 10:
            self.velocity = 0.50
        elif 10 < counter <= 15:
            self.velocity = 0.60
        elif 15 < counter <= 20:
            self.velocity = 0.70
        elif 20 < counter <= 25:
            self.velocity = 0.80
        elif 25 < counter <= 30:
            self.velocity = 0.90
        elif 30 < counter <= 35:
            self.velocity = 1.00
        elif 35 < counter <= 40:
            self.velocity = 1.10
        elif 40 < counter <= 45:
            self.velocity = 1.20
        elif 45 < counter <= 50:
            self.velocity = 1.30
        elif 50 < counter <= 60:
            self.velocity = 1.40
        elif 60 < counter <= 70:
            self.velocity = 1.50
        elif 70 < counter <= 80:
            self.velocity = 1.60
        elif 80 < counter <= 90:
            self.velocity = 1.70
        elif 90 < counter <= 100:
            self.velocity = 1.80
        elif counter > 100:
            self.velocity = 1.80  # Cap max speed

        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN] and self.player.y >= FLOOR:
            if self.player.height != PLAYER_SIZE // 2:
                self.player.y += PLAYER_SIZE // 2
                self.player.height = PLAYER_SIZE // 2
        else:
            if self.player.height != PLAYER_SIZE:
                self.player.y -= PLAYER_SIZE // 2
                self.player.height = PLAYER_SIZE

        self.mouse_pos = pygame.mouse.get_pos()
        if self.mouse_pos[1] < SCREEN_HEIGHT // 2 and pygame.mouse.get_pressed()[0] and self.player.y == FLOOR:
            if self.player.height != PLAYER_SIZE // 2:
                self.player.y += PLAYER_SIZE // 2
                self.player.height = PLAYER_SIZE // 2

        for obj in objects:
            if self.player.colliderect(obj):
                self.health -= 1
                objects.remove(obj)

        if self.health <= 0:
            if counter > high_score:
                high_score = counter
            counter = 0
            game_state = "menu"
            restart = True

        # Jump physics
        if self.is_jumping:
            self.player.y -= self.gravity
            self.gravity += self.velocity * delta_time * 60

        if self.is_jumping and self.player.y <= FLOOR - SLOW_DOWN_HEIGHT:
            self.is_jumping = False
            self.slow_down = True

        if self.slow_down:
            if self.gravity >= 0.5:
                self.player.y -= self.gravity
                self.gravity -= self.velocity * delta_time * 60
            else:
                self.slow_down = False
                self.is_falling = True

        if self.slow_down and self.player.y <= FLOOR - JUMP_HEIGHT:
            self.gravity = 0.5
            self.slow_down = False
            self.is_falling = True

        if self.is_falling:
            self.player.y += self.gravity
            self.gravity += self.velocity * delta_time * 60

        if self.is_falling and self.player.y >= FLOOR:
            self.player.y = FLOOR
            self.gravity = 0.5
            self.is_falling = False

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE and
                self.player.height == PLAYER_SIZE and
                not self.is_jumping and
                not self.is_falling and
                not self.slow_down):
                self.is_jumping = True

        if (event.type == pygame.MOUSEBUTTONDOWN and
            event.button == 1 and
            pygame.mouse.get_pos()[1] > SCREEN_HEIGHT // 2 and
            self.player.height == PLAYER_SIZE and
            not self.is_jumping and
            not self.is_falling and
            not self.slow_down):
            self.is_jumping = True

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.player)
        for i in range(self.health):
            pygame.draw.circle(surface, WHITE, ((SCREEN_WIDTH - 100) - 50 * i, 50), 15, 1)


# -------------------- ENVIRONMENT --------------------

class Environment:
    def __init__(self):
        self.floor = pygame.Rect(0, FLOOR + PLAYER_SIZE, SCREEN_WIDTH, 1)
        self.object_speed = 4
        self.objects = []
        self.time_accumulator = 0

    def update(self, delta_time, **kwargs):
        global counter

        # Adjust difficulty based on score
        if counter <= 5:
            self.object_speed = 4.0
        elif 5 < counter <= 10:
            self.object_speed = 4.5
        elif 10 < counter <= 15:
            self.object_speed = 5.0
        elif 15 < counter <= 20:
            self.object_speed = 5.5
        elif 20 < counter <= 25:
            self.object_speed = 6.0
        elif 25 < counter <= 30:
            self.object_speed = 6.5
        elif 30 < counter <= 35:
            self.object_speed = 7.0
        elif 35 < counter <= 40:
            self.object_speed = 7.5
        elif 40 < counter <= 45:
            self.object_speed = 8.0
        elif 45 < counter <= 50:
            self.object_speed = 8.5
        elif 50 < counter <= 60:
            self.object_speed = 9.0
        elif 60 < counter <= 70:
            self.object_speed = 9.5
        elif 70 < counter <= 80:
            self.object_speed = 10.0
        elif 80 < counter <= 90:
            self.object_speed = 10.5
        elif 90 < counter <= 100:
            self.object_speed = 11.0
        elif counter > 100:
            self.object_speed = 12.0

        for obj in self.objects:
            obj.x -= self.object_speed * delta_time * 60

        self.objects = [obj for obj in self.objects if obj.x > -100]

        if len(self.objects) < 3:
            last_x = self.objects[-1].x if self.objects else 0
            new_x = max(SCREEN_WIDTH, last_x + 450 + random.randint(0, 800))
            if random.choice([True, False]):
                self.objects.append(pygame.Rect(new_x, FLOOR + PLAYER_SIZE - TREE_HEIGHT, TREE_WIDTH, TREE_HEIGHT))
            else:
                self.objects.append(pygame.Rect(new_x, FLOOR, BIRD_WIDTH, BIRD_HEIGHT))

        # Increase counter every second (not every frame)
        self.time_accumulator += delta_time
        if self.time_accumulator >= 1.0:
            counter += 1
            self.time_accumulator = 0

    def handle_events(self, **kwargs):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.floor)
        for obj in self.objects:
            pygame.draw.rect(surface, WHITE, obj)
        draw_text(surface, f"{counter}", 15, WHITE, (50, 50), True)


# -------------------- MENU --------------------

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
                                  SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2,
                                  BUTTON_WIDTH, BUTTON_HEIGHT)

    def update(self, **kwargs):
        pass

    def handle_events(self):
        global game_state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button.collidepoint(pygame.mouse.get_pos()):
                    game_state = "running"

    def draw(self):
        self.surface.fill(GREY)
        pygame.draw.rect(self.surface, LIGHT_GREY, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        draw_text(self.surface, "CROUCH", 25, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        draw_text(self.surface, "JUMP", 25, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
        pygame.draw.rect(self.surface, BLACK, self.button)
        draw_text(self.surface, "START", 32, WHITE, self.button.center)
        draw_text(self.surface, f"HIGH SCORE: {high_score}", 25, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()


# -------------------- GAME --------------------

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Blockasaurus")
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen)
        self.environment = Environment()
        self.player = Player()
        self.entities = [self.player, self.environment]

    def update(self, delta_time):
        for entity in self.entities:
            entity.update(objects=self.environment.objects, delta_time=delta_time)

    def handle_events(self):
        global game_state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "stop"
            for entity in self.entities:
                entity.handle_events(event=event)

    def draw(self):
        self.screen.fill(GREY)
        for entity in self.entities:
            entity.draw(self.screen)
        pygame.display.flip()

    def reset(self):
        self.environment = Environment()
        self.player = Player()
        self.entities = [self.player, self.environment]

    async def run(self):
        global restart, game_state

        while game_state != "stop":
            delta_time = self.clock.tick(60) / 1000  # normalize to seconds

            if game_state == "menu":
                self.menu.draw()
                self.menu.handle_events()
                if restart:
                    self.reset()
                    restart = False
            elif game_state == "running":
                self.handle_events()
                self.update(delta_time)
                self.draw()

            await asyncio.sleep(0)  # Pygbag yield


# -------------------- MAIN --------------------

async def main():
    game = Game()
    await game.run()

import asyncio
asyncio.run(main())