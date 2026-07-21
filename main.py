"""A graphical Jigglypuff Sleep Timer featuring a radial progress ring UI."""

import argparse
import logging
import math
import os
import sys
import time
import gif_pygame
import pygame
from engine import TimerEngine

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s", 
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# UI Design Palette (Jigglypuff Theme)
COLOR_BG = (42, 28, 36)           # Deep, dark pastel plum
COLOR_TEXT_MAIN = (255, 230, 235) # Creamy pastel pink for countdown display
COLOR_RING_BG = (65, 45, 56)      # Subdued tracking rail ring
COLOR_BAR_FILL = (0, 168, 181)    # Luminous teal-blue matching Jigglypuff's eyes
COLOR_BAR_FADE = (175, 90, 105)   # Warm rose shadow used during fade window


def verify_assets(*asset_paths: str) -> None:
    """Ensure all required media and font files exist before initialising Pygame."""
    missing = [path for path in asset_paths if not os.path.exists(path)]
    if missing:
        logger.error("Missing required assets or fonts:")
        for path in missing:
            logger.error(f"  ❌ {path}")
        sys.exit(1)


def draw_radial_progress(surface: pygame.Surface, rect: pygame.Rect, progress: float, color: tuple) -> None:
    """Draw a clockwise radial progress arc starting at 12 o'clock."""
    if progress <= 0:
        return
        
    # Pygame arc angles increase anti-clockwise from 3 o'clock (0 rad).
    # Shift by -pi/2 to start at 12 o'clock and sweep clockwise.
    start_angle = -math.pi / 2
    end_angle = start_angle + (2 * math.pi * progress)
    
    pygame.draw.arc(surface, color, rect, start_angle, end_angle, width=8)


def run_timer(duration_mins: float, fade_mins: float, audio_path: str, gif_path: str) -> None:
    """Initialises a fullscreen window and executes the timer loop."""
    font_bold_path = "assets/GoogleSans-Bold.ttf"
    font_regular_path = "assets/GoogleSans-Regular.ttf"
    verify_assets(audio_path, gif_path, font_bold_path, font_regular_path)

    try:
        engine = TimerEngine(duration_mins * 60, fade_mins * 60)
    except ValueError as err:
        logger.error(f"Configuration error: {err}")
        sys.exit(1)

    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Jigglypuff Lullaby Room")
    screen_w, screen_h = screen.get_size()
    
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    font_large = pygame.font.Font(font_bold_path, 48)
    pygame.mixer.music.load(audio_path)
    jiggly_gif = gif_pygame.load(gif_path)

    # Offset character and timer to sit comfortably in top/bottom screen halves
    gif_w, gif_h = jiggly_gif.get_width(), jiggly_gif.get_height()
    jiggly_pos = ((screen_w - gif_w) // 2, (screen_h // 2) - gif_h - 20)

    center_x, center_y = screen_w // 2, (screen_h // 2) + 120
    radius = 90
    arc_rect = pygame.Rect(center_x - radius, center_y - radius, radius * 2, radius * 2)

    pygame.mixer.music.play(loops=-1)
    start_time = time.time()
    logger.info("Jigglypuff has entered the screen...")
    
    running = True
    in_blackout = False
    blackout_end_time = 0.0

    while running:
        current_time = time.time()
        elapsed_secs = current_time - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        if not in_blackout:
            pygame.mixer.music.set_volume(engine.get_volume(elapsed_secs))
            ui = engine.get_ui_metrics(elapsed_secs)

            if ui["phase"] == "BLACKOUT":
                logger.info("Timer expired. Starting 10-second blackout phase...")
                pygame.mixer.music.stop()
                in_blackout = True
                blackout_end_time = current_time + 10.0
            else:
                screen.fill(COLOR_BG)
                jiggly_gif.render(screen, jiggly_pos)
                pygame.draw.circle(screen, COLOR_RING_BG, (center_x, center_y), radius, width=8)

                arc_color = COLOR_BAR_FADE if ui["phase"] == "FADING" else COLOR_BAR_FILL
                draw_radial_progress(screen, arc_rect, ui["progress"], arc_color)

                time_surface = font_large.render(ui["time_string"], True, COLOR_TEXT_MAIN)
                text_rect = time_surface.get_rect(center=(center_x, center_y))
                screen.blit(time_surface, text_rect)
        else:
            if current_time >= blackout_end_time:
                running = False
            else:
                screen.fill((0, 0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.mouse.set_visible(True)
    pygame.mixer.quit()
    pygame.quit()
    logger.info("Timer complete. Screen restored.")


def main() -> None:
    """CLI Parsing entry point."""
    parser = argparse.ArgumentParser(description="Jigglypuff visual sleep timer.")
    parser.add_argument("-d", "--duration", type=float, default=1.0, help="Duration in minutes")
    parser.add_argument("-f", "--fade", type=float, default=0.2, help="Audio fade window in minutes")
    parser.add_argument("-a", "--audio", type=str, default="assets/lullaby.mp3")
    parser.add_argument("-g", "--gif", type=str, default="assets/jigglypuff.gif")

    args = parser.parse_args()
    run_timer(args.duration, args.fade, args.audio, args.gif)


if __name__ == "__main__":
    main()