import pygame
import math
import random
import time

class Player(): # Generated slime
    def __init__(self, pos=(0, 0), size=90):
        self.pos = list(pos)
        self.size = size
        self.color = pygame.Color(0, 255, 0)
        self.surface = self.update_surface()

    def update_surface(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color, (self.size // 2, self.size // 2), self.size // 2)
        return surf

    def draw(self, surface):
        surface.blit(self.surface, self.pos)

    def move(self, keys): # movement
        speed = 5
        if keys[pygame.K_w]:
            self.pos[1] -= speed
        if keys[pygame.K_s]:
            self.pos[1] += speed
        if keys[pygame.K_a]:
            self.pos[0] -= speed
        if keys[pygame.K_d]:
            self.pos[0] += speed

class SmallCircle():
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.color = pygame.Color(random.randrange(256), random.randrange(256), random.randrange(256))
        self.surface = self.update_surface()

    def update_surface(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color, (self.size // 2, self.size // 2), self.size // 2)
        return surf

    def draw(self, surface):
        surface.blit(self.surface, self.pos)

class Game(): # Clearing the game 
    def __init__(self, resolution):
        self.resolution = resolution
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Slime Collection!")
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.points = 0
        self.player = Player(pos=(resolution[0] // 2, resolution[1] // 2), size=90)
        self.small_circles = self.generate_small_circles(10)
        self.win = False
        self.win_timer = 0
        self.win_display_time = 3
        self.flash_duration = 1.0  
        self.last_flash_time = 0

    def generate_small_circles(self, count): # generates slime balls to collect
        small_circles = []
        for _ in range(count):
            x = random.randrange(self.resolution[0])
            y = random.randrange(self.resolution[1])
            size = random.randint(10, 30)
            small_circle = SmallCircle(pos=(x, y), size=size)
            small_circles.append(small_circle)
        return small_circles

    def check_collisions(self): # method to collect the slime balls
        for small_circle in self.small_circles:
            distance = math.dist((self.player.pos[0] + self.player.size // 2, self.player.pos[1] + self.player.size // 2),
                                (small_circle.pos[0] + small_circle.size // 2, small_circle.pos[1] + small_circle.size // 2))
            if distance < (self.player.size + small_circle.size) // 2:
                self.points += 1
                self.small_circles.remove(small_circle)
                self.small_circles.append(SmallCircle(pos=(random.randrange(self.resolution[0]), random.randrange(self.resolution[1])),
                                                      size=random.randint(10, 30)))
                if self.points == 10:
                    self.win = True
                    self.win_timer = time.time()

    def draw_points(self): # points
        font = pygame.font.Font(None, 36)
        text = font.render(f"Points: {self.points}", True, pygame.Color(255, 255, 255))
        self.screen.blit(text, (self.resolution[0] - 150, 20))

    def draw_win_message(self): # win message 
        current_time = time.time()
        if current_time - self.last_flash_time > self.flash_duration:
            self.last_flash_time = current_time
            return True

        font = pygame.font.Font(None, 144)
        rainbow_colors = [pygame.Color(255, 0, 0), pygame.Color(255, 165, 0), pygame.Color(255, 255, 0),
                          pygame.Color(0, 128, 0), pygame.Color(0, 0, 255), pygame.Color(75, 0, 130),
                          pygame.Color(238, 130, 238)]
        text = font.render("You win!", True, random.choice(rainbow_colors))
        text_rect = text.get_rect(center=(self.resolution[0] // 2, self.resolution[1] // 2))
        self.screen.blit(text, text_rect)

    def run(self): # End game methods
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            if not self.win:
                keys = pygame.key.get_pressed()
                self.player.move(keys)

                self.check_collisions()

                black = pygame.Color(0, 0, 0)
                self.screen.fill(black)

                for small_circle in self.small_circles:
                    small_circle.draw(self.screen)

                self.player.draw(self.screen)

                self.draw_points()
            else:
                if self.draw_win_message() and time.time() - self.win_timer > self.win_display_time:
                    self.win = False
                    self.points = 0
                    self.small_circles = self.generate_small_circles(10)

            pygame.display.flip()
            self.dt = self.clock.tick(60)

        pygame.quit()

def main():
    pygame.init()
    game = Game((1920, 1080))
    game.run()

if __name__ == "__main__":
    main()
