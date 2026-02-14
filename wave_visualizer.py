#!/usr/bin/env python3
"""Wave Gremlin – a tiny interactive wave function visualizer using Pygame."""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

import pygame

WIDTH, HEIGHT = 960, 480
BACKGROUND = (12, 12, 16)
WAVE_COLOR = (80, 200, 255)
GRID_COLOR = (40, 40, 52)
TEXT_COLOR = (220, 220, 230)


@dataclass
class WaveParams:
    amplitude: float = 100.0  # pixels
    frequency: float = 2.0  # waves per screen width
    speed: float = 120.0  # pixels per second (phase velocity)

    def clamp(self) -> None:
        self.amplitude = max(10.0, min(self.amplitude, HEIGHT / 2 - 10))
        self.frequency = max(0.2, min(self.frequency, 6.0))
        self.speed = max(10.0, min(self.speed, 400.0))


class WaveVisualizer:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Wave Gremlin")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("ibmplexmono", 18)
        self.params = WaveParams()
        self.phase = 0.0

    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            running = self.handle_events(dt)
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self, dt: float) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    return False
                if event.key == pygame.K_r:
                    self.params = WaveParams()
                    self.phase = 0.0

        keys = pygame.key.get_pressed()
        delta = 60 * dt  # normalize to roughly per-second adjustments
        if keys[pygame.K_UP]:
            self.params.amplitude += 30 * delta
        if keys[pygame.K_DOWN]:
            self.params.amplitude -= 30 * delta
        if keys[pygame.K_LEFT]:
            self.params.frequency -= 0.8 * delta
        if keys[pygame.K_RIGHT]:
            self.params.frequency += 0.8 * delta
        if keys[pygame.K_a]:
            self.params.speed -= 120 * delta
        if keys[pygame.K_z]:
            self.params.speed += 120 * delta

        self.params.clamp()
        return True

    def update(self, dt: float) -> None:
        # advance phase based on speed
        self.phase += (self.params.speed * dt)

    def draw(self) -> None:
        self.screen.fill(BACKGROUND)
        self._draw_grid()
        self._draw_wave()
        self._draw_hud()
        pygame.display.flip()

    def _draw_grid(self) -> None:
        for x in range(0, WIDTH, 80):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 80):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y), 1)
        pygame.draw.line(
            self.screen, (60, 60, 80), (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1
        )

    def _draw_wave(self) -> None:
        points = []
        angular_frequency = self.params.frequency * 2 * math.pi / WIDTH
        for x in range(WIDTH):
            offset = math.sin(self.phase * angular_frequency + x * angular_frequency)
            y = HEIGHT // 2 + offset * self.params.amplitude
            points.append((x, y))
        if len(points) > 1:
            pygame.draw.lines(self.screen, WAVE_COLOR, False, points, 2)

    def _draw_hud(self) -> None:
        lines = [
            f"Amplitude: {self.params.amplitude:5.1f} px",
            f"Frequency: {self.params.frequency:4.2f} waves/width",
            f"Speed: {self.params.speed:5.1f} px/s",
            "Controls: ↑↓ amp | ←→ freq | A/Z speed | R reset | Esc/Q quit",
        ]
        for idx, text in enumerate(lines):
            surface = self.font.render(text, True, TEXT_COLOR)
            self.screen.blit(surface, (16, 16 + idx * 22))


def main() -> None:
    visualizer = WaveVisualizer()
    visualizer.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit(0)
