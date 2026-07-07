"""A graphical Jigglypuff Sleep Timer with an animated GIF and blackout sequence."""

import argparse
import logging
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


def run_timer(duration_mins: float, fade_mins: float, audio_path: str, gif_path: str) -> None:
    """Initialises a fullscreen window, plays a loop, and transitions to a blackout."""
    # Convert input settings to seconds
    duration_secs = duration_mins * 60
    fade_secs = fade_mins * 60

    # Instantiate our pure mathematical state engine
    try:
        engine = TimerEngine(duration_secs, fade_secs)
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)

    pygame.init()
    pygame.mixer.init()

    # Initialise a borderless fullscreen window matching native resolution
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Jigglypuff Lullaby Room")
    screen_width, screen_height = screen.get_size()
    
    # Hide the system cursor inside our canvas space
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # Load media files
    try:
        pygame.mixer.music.load(audio_path)
        jiggly_gif = gif_pygame.load(gif_path)
    except FileNotFoundError as e:
        logger.error(f"Asset file error: {e}")
        pygame.quit()
        sys.exit(1)

    # Centre position calculations for the GIF animation
    gif_w, gif_h = jiggly_gif.get_width(), jiggly_gif.get_height()
    center_x = (screen_width - gif_w) // 2
    center_y = (screen_height - gif_h) // 2

    # Start the loops
    pygame.mixer.music.play(loops=-1)
    start_time = time.time()
    
    logger.info("Jigglypuff has entered the screen...")
    
    running = True
    in_blackout = False
    blackout_end_time = 0.0

    while running:
        current_time = time.time()
        elapsed_secs = current_time - start_time
        
        # Check system window events to ensure safe exits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    logger.info("Override triggered via Escape key.")
                    running = False

        if not in_blackout:
            # Query our engine for the volume state based on pure elapsed time
            volume = engine.get_volume(elapsed_secs)
            pygame.mixer.music.set_volume(volume)

            # Stage 1: Active Playback and Fading Loop
            if elapsed_secs >= duration_secs:
                # Transition to blackout state
                logger.info("Timer expired. Starting 10-second blackout phase...")
                pygame.mixer.music.stop()
                in_blackout = True
                blackout_end_time = current_time + 10.0
            else:
                # Render Phase: Dark background and centred animated GIF
                screen.fill((20, 20, 30))
                jiggly_gif.render(screen, (center_x, center_y))
        else:
            # Stage 2: The Blackout Window
            if current_time >= blackout_end_time:
                running = False
            else:
                # Render Phase: Complete pitch black canvas
                screen.fill((0, 0, 0))

        pygame.display.flip()
        clock.tick(60)  # Keep execution locked at 60 FPS

    # Clean cleanup sequence
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