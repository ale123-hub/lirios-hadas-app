import streamlit as st
import pygame
import math
import random
import numpy as np

# Configuración de la página en Streamlit
st.set_page_config(page_title="Lirios Amarillos y Hadas de Luz", layout="centered")
st.title("✨ Lirios Amarillos y Hadas de Luz")

# Inicialización de Pygame en modo sin cabeza (headless)
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.Surface((WIDTH, HEIGHT))

# Colores
NIGHT_BLUE = (10, 15, 35)
MOON_WHITE = (245, 245, 230)
YELLOW_PETAL = (255, 215, 0)
YELLOW_CENTER = (255, 165, 0)
GREEN_STEM = (34, 139, 34)
DARK_GREEN = (0, 70, 20)
VERY_DARK_GREEN = (0, 35, 10)

# Generación de estrellas estáticas
stars = [(random.randint(0, WIDTH), random.randint(0, 350), random.randint(1, 2)) for _ in range(80)]

# Generación de hojas de césped (x, alto, inclinación base, fase de viento)
grass_blades = [
    (x, random.randint(15, 45), random.uniform(-0.3, 0.3), random.uniform(0, math.pi * 2))
    for x in range(0, WIDTH, 4)
]

class FairyParticle:
    """Clase para simular el brillo flotante de las hadas."""
    def __init__(self, x, y):
        self.base_x = x
        self.base_y = y
        self.x = x
        self.y = y
        self.size = random.uniform(2, 5)
        self.speed = random.uniform(0.02, 0.05)
        self.angle = random.uniform(0, math.pi * 2)
        self.radius = random.uniform(15, 40)
        self.alpha = random.randint(150, 255)
        
    def update(self):
        self.angle += self.speed
        # Movimiento suave tipo flotación
        self.x = self.base_x + math.cos(self.angle) * self.radius + math.sin(self.angle * 2) * 10
        self.y = self.base_y + math.sin(self.angle) * self.radius + math.cos(self.angle * 1.5) * 10
        # Parpadeo de luz
        self.alpha = int(180 + 75 * math.sin(self.angle * 3))

    def draw(self, surface):
        s = pygame.Surface((int(self.size * 4), int(self.size * 4)), pygame.SRCALPHA)
        # Resplandor exterior
        pygame.draw.circle(s, (255, 235, 150, max(0, self.alpha // 3)), (int(self.size * 2), int(self.size * 2)), int(self.size * 2))
        # Núcleo brillante
        pygame.draw.circle(s, (255, 255, 255, self.alpha), (int(self.size * 2), int(self.size * 2)), int(self.size))
        surface.blit(s, (int(self.x - self.size * 2), int(self.y - self.size * 2)))

def draw_moon(surface):
    # Resplandor suave de la luna
    for r in range(80, 50, -5):
        alpha = int(5 * (80 - r))
        glow_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (220, 235, 255, alpha), (r, r), r)
        surface.blit(glow_surf, (650 - r, 120 - r))
    # Luna principal
    pygame.draw.circle(surface, MOON_WHITE, (650, 120), 45)

def draw_grass(surface):
    """Suelo de césped con colinas suaves y hebras animadas con el viento."""
    time = pygame.time.get_ticks() * 0.002
    
    # 1. Base del prado (silueta en capa)
    pygame.draw.ellipse(surface, VERY_DARK_GREEN, (-100, 500, WIDTH + 200, 200))
    pygame.draw.ellipse(surface, DARK_GREEN, (-50, 530, WIDTH + 100, 150))

    # 2. Hebras individuales de césped meciéndose
    for x, height, bend, phase in grass_blades:
        wind = math.sin(time + phase) * 6
        top_x = x + bend * 10 + wind
        top_y = HEIGHT - height
        
        # Color variante para dar profundidad
        color = DARK_GREEN if x % 8 == 0 else GREEN_STEM
        pygame.draw.line(surface, color, (x, HEIGHT), (top_x, top_y), 2)

def draw_lily(surface, x, base_y, height, scale=1.0):
    flower_top_y = base_y - height
    
    # Tallos curvos
    control_x = x + math.sin(pygame.time.get_ticks() * 0.001) * 10
    points = [(x, base_y), (control_x, base_y - height // 2), (x, flower_top_y)]
    pygame.draw.lines(surface, GREEN_STEM, False, points, max(2, int(6 * scale)))

    # Hojas alargadas
    pygame.draw.arc(surface, DARK_GREEN, (x - 40 * scale, base_y - 80 * scale, 50 * scale, 80 * scale), 0, math.pi/2, max(1, int(4 * scale)))
    pygame.draw.arc(surface, DARK_GREEN, (x - 10 * scale, base_y - 110 * scale, 50 * scale, 80 * scale), math.pi/2, math.pi, max(1, int(4 * scale)))

    # Pétalos del lirio
    petal_angle_step = math.pi / 3
    for i in range(6):
        angle = i * petal_angle_step - math.pi / 2
        p_x = x + math.cos(angle) * (45 * scale)
        p_y = flower_top_y + math.sin(angle) * (55 * scale)
        
        ctrl1_x = x + math.cos(angle - 0.4) * (25 * scale)
        ctrl1_y = flower_top_y + math.sin(angle - 0.4) * (25 * scale)
        ctrl2_x = x + math.cos(angle + 0.4) * (25 * scale)
        ctrl2_y = flower_top_y + math.sin(angle + 0.4) * (25 * scale)

        petal_points = [(x, flower_top_y), (ctrl1_x, ctrl1_y), (p_x, p_y), (ctrl2_x, ctrl2_y)]
        pygame.draw.polygon(surface, YELLOW_PETAL, petal_points)
        pygame.draw.polygon(surface, (218, 165, 32), petal_points, 1)

    # Centro y pistilos
    pygame.draw.circle(surface, YELLOW_CENTER, (int(x), int(flower_top_y)), max(3, int(8 * scale)))
    for i in range(5):
        stamen_angle = i * (math.pi / 2.5) - math.pi / 1.2
        st_x = x + math.cos(stamen_angle) * (18 * scale)
        st_y = flower_top_y + math.sin(stamen_angle) * (18 * scale)
        pygame.draw.line(surface, YELLOW_CENTER, (x, flower_top_y), (st_x, st_y), max(1, int(2 * scale)))
        pygame.draw.circle(surface, (139, 69, 19), (int(st_x), int(st_y)), max(2, int(3 * scale)))

# Posiciones de lirios
lily_positions = [
    (120, 580, 160, 0.75),
    (220, 585, 210, 0.95),
    (340, 595, 240, 1.1),
    (450, 580, 180, 0.85),
    (560, 600, 260, 1.2),
    (670, 585, 200, 0.9),
    (740, 575, 150, 0.7)
]

fairies = []
for x, b_y, h, sc in lily_positions:
    f_y = b_y - h
    for _ in range(10):  # Partículas por flor
        fairies.append(FairyParticle(x + random.randint(-25, 25), f_y + random.randint(-25, 25)))

# Espacio reservado para renderizar el lienzo de la animación en Streamlit
frame_placeholder = st.empty()

# Bucle infinito para actualizar la animación en la web
while True:
    screen.fill(NIGHT_BLUE)

    # Dibujar estrellas
    for sx, sy, ssize in stars:
        pygame.draw.circle(screen, (255, 255, 255), (sx, sy), ssize)

    # Dibujar Luna
    draw_moon(screen)

    # Dibujar Césped
    draw_grass(screen)

    # Dibujar Lirios
    for x, base_y, height, scale in lily_positions:
        draw_lily(screen, x, base_y, height, scale)

    # Actualizar y dibujar hadas
    for fairy in fairies:
        fairy.update()
        fairy.draw(screen)

    # Convertir el lienzo de Pygame a formato de imagen para Streamlit
    img_array = pygame.surfarray.array3d(screen)
    img_array = np.transpose(img_array, (1, 0, 2))

    # Mostrar el fotograma actual en la web
    frame_placeholder.image(img_array, width="stretch")