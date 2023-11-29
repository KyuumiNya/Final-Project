import pygame
import math

class Player():
    def __init__(self, pos=(0, 0), size=30):
        self.pos = list(pos)
        self.size = size
        self.color = pygame.Color(0, 255, 0)  # Green color
        self.surface = self.update_surface()

    def update_surface(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color, (self.size // 2, self.size // 2), self.size // 2)
        return surf

    def draw(self, surface):
        surface.blit(self.surface, self.pos)

    def move(self, keys):
        speed = 5
        if keys[pygame.K_w]:
            self.pos[1] -= speed
        if keys[pygame.K_s]:
            self.pos[1] += speed
        if keys[pygame.K_a]:
            self.pos[0] -= speed
        if keys[pygame.K_d]:
            self.pos[0] += speed

def main():
    pygame.init()
    pygame.display.set_caption("Larger Circular Pixel Move")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    player = Player(pos=(resolution[0] // 2, resolution[1] // 2), size=60)  # Adjust the size here

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.move(keys)

        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        player.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
