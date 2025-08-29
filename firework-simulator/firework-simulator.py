import pygame
import random
import math

pygame.init()

# Fullscreen automático
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("ASCII Fireworks - Fase2 más grande")

FPS = 60
clock = pygame.time.Clock()

# Caracteres por fase
PHASE1 = ["o", "O", "●"]      # menos puntos
PHASE2 = ["$", "#", "!", "="] # más visibles
PHASE3 = ["|", "¦", "!"]

MAX_FIREWORKS = 70
font_size = 20  # caracteres pequeños
font = pygame.font.SysFont("monospace", font_size)

# Colores vivos
COLOR_POOL = [(255,0,0),(255,255,0),(0,255,0),(0,255,255),(255,0,255),(255,128,0),(128,0,255)]

class Particle:
    def __init__(self, x, y, char, color, vx=0, vy=0, phase=1, lifespan=30):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.vx = vx
        self.vy = vy
        self.age = 0
        self.alive = True
        self.phase = phase
        self.lifespan = lifespan

    def update(self):
        if self.phase in [1,2]:
            self.x += self.vx
            self.y += self.vy
            self.vy += 0.12
            self.vx *= 0.995
            self.age += 1
            if self.phase == 1 and self.age == 6:
                self.char = random.choice(PHASE2)
                self.phase = 2
            if self.age > self.lifespan:
                self.alive = False
        elif self.phase == 3:
            self.y += self.vy
            self.vy += 0.05
            if self.y > HEIGHT:
                self.alive = False

class Firework:
    def __init__(self):
        self.cx = random.randint(50, WIDTH-50)
        self.cy = random.randint(30, HEIGHT//2)
        self.particles = []
        self.phase3_done = False
        self.max_particles = random.randint(25, 40)  # menos puntos
        self.spawned = 0
        # Paleta de 3 colores vivos
        self.palette = random.sample(COLOR_POOL, 3)
        # Núcleo central
        self.particles.append(Particle(self.cx, self.cy, "●", self.palette[0], lifespan=40))

    def update(self):
        # Generar partículas gradualmente
        if self.spawned < self.max_particles:
            for _ in range(2):
                angle = random.uniform(0,2*math.pi)
                speed = random.uniform(2,5)
                # Algunas partículas se expanden más lejos
                if random.random() < 0.25:
                    speed *= 1.7
                vx = math.cos(angle)*speed
                vy = -math.sin(angle)*speed
                color = random.choice(self.palette)
                # Mayor chance de fase2 para que sean visibles
                char = random.choices(PHASE1+PHASE2, weights=[1,1,1,3,3,3,3])[0]
                self.particles.append(Particle(self.cx, self.cy, char, color, vx, vy, lifespan=random.randint(35,45)))
                self.spawned += 1
                if self.spawned >= self.max_particles:
                    break

        any_alive = False
        for p in self.particles:
            p.update()
            if p.alive:
                any_alive = True

        # Phase3 rain
        if not self.phase3_done and all(p.phase==2 and not p.alive for p in self.particles if hasattr(p,'phase')):
            for _ in range(random.randint(6,10)):
                self.particles.append(Particle(self.cx+random.uniform(-10,10), self.cy,
                                               random.choice(PHASE3), random.choice(self.palette),
                                               vy=random.uniform(2,4), phase=3, lifespan=random.randint(35,45)))
            self.phase3_done = True
            any_alive = True

        return any_alive

    def draw(self, surf):
        for p in self.particles:
            if p.alive:
                text = font.render(p.char, True, p.color)
                surf.blit(text, (p.x,p.y))

def main():
    running = True
    fireworks = []

    while running:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(fireworks) < MAX_FIREWORKS:
                        fireworks.append(Firework())
                elif event.key == pygame.K_q:
                    running = False

        # Update fireworks
        fireworks_alive = []
        for fw in fireworks:
            if fw.update():
                fireworks_alive.append(fw)
        fireworks = fireworks_alive

        # Draw fireworks
        for fw in fireworks:
            fw.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__=="__main__":
    main()

