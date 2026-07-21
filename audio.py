"""Audio subsystem for the Jigglypuff Lullaby Sleep Timer."""

import logging
import time
from pathlib import Path

import pygame

logger = logging.getLogger(__name__)


class LullabyPlayer:
    """Manages background audio playback and smooth volume fading."""

    def __init__(self, audio_path: str) -> None:
        """Initialises the player state and verifies asset existence.

        Args:
            audio_path: Path to the lullaby audio file.

        Raises:
            FileNotFoundError: If the specified audio file does not exist.
        """
        self.audio_path = Path(audio_path)
        if not self.audio_path.exists():
            raise FileNotFoundError(f"Lullaby audio file not found at: {audio_path}")

    def play_and_fade(self, duration_seconds: float, fade_seconds: float) -> None:
        """Plays the lullaby loop and smoothly fades out over the specified window.

        Args:
            duration_seconds: Total playback duration in seconds.
            fade_seconds: Duration of the fade-out window prior to stopping.
        """
        pygame.mixer.init()
        pygame.mixer.music.load(str(self.audio_path))
        pygame.mixer.music.play(loops=-1)

        start_time = time.time()
        end_time = start_time + duration_seconds
        fade_start_time = end_time - fade_seconds

        logger.info("Jigglypuff has started singing...")

        try:
            while True:
                current_time = time.time()
                if current_time >= end_time:
                    break

                if current_time >= fade_start_time:
                    remaining_fade_time = end_time - current_time
                    
                    # Linear decay formula: V(t) = max_volume * (remaining_fade / total_fade)
                    volume = max(0.0, min(1.0, remaining_fade_time / fade_seconds))
                    pygame.mixer.music.set_volume(volume)

                time.sleep(0.1)  # Brief polling pause to avoid high CPU usage
        finally:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            logger.info("The lullaby has finished.")