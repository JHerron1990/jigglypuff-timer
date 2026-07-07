"""Audio subsystem for the Jigglypuff Lullaby Sleep Timer."""

import logging
import time
from pathlib import Path
import pygame

logger = logging.getLogger(__name__)


class LullabyPlayer:
    """Manages background audio playback and smooth volume fading."""

    def __init__(self, audio_path: str) -> None:
        self.audio_path = audio_path
        pygame.mixer.init()
        
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Lullaby audio file not found at: {audio_path}")

    def play_and_fade(self, duration_seconds: float, fade_seconds: float) -> None:
        """Plays the lullaby loop and smoothly fades out over the specified window."""
        pygame.mixer.music.load(self.audio_path)
        # Play on an infinite loop (-1)
        pygame.mixer.music.play(loops=-1)
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        fade_start_time = end_time - fade_seconds

        logger.info("Jigglypuff has started singing...")

        while True:
            current_time = time.time()
            if current_time >= end_time:
                break

            # If we enter the fading window, mathematically decay the volume
            if current_time >= fade_start_time:
                remaining_fade_time = end_time - current_time
                # Linear volume calculation: V(t) = max_volume * (remaining_fade / total_fade)
                volume = max(0.0, min(1.0, remaining_fade_time / fade_seconds))
                pygame.mixer.music.set_volume(volume)

            time.sleep(1.0)

        pygame.mixer.music.stop()
        pygame.mixer.quit()
        logger.info("The lullaby has finished.")