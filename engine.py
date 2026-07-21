"""Pure mathematical state engine for the timer with UI metrics."""

from typing import TypedDict


class UIMetrics(TypedDict):
    """Container for UI rendering metrics."""

    time_string: str
    progress: float
    phase: str


class TimerEngine:
    """Manages timer state and volume calculations independently of hardware."""

    def __init__(self, duration_secs: float, fade_secs: float) -> None:
        """Initialises the timer engine configuration.

        Args:
            duration_secs: Total timer duration in seconds.
            fade_secs: Audio fade-out duration window in seconds.

        Raises:
            ValueError: If fade duration exceeds total duration.
        """
        if fade_secs > duration_secs:
            raise ValueError("Fade duration cannot be longer than total duration.")

        self.duration_secs = duration_secs
        self.fade_secs = fade_secs

    def get_volume(self, elapsed_secs: float) -> float:
        """Calculates the target volume level based on elapsed time.

        Args:
            elapsed_secs: Time elapsed since the timer started.

        Returns:
            Float representing audio volume, constrained between 0.0 and 1.0.
        """
        if elapsed_secs >= self.duration_secs:
            return 0.0

        fade_start = self.duration_secs - self.fade_secs
        if elapsed_secs < fade_start:
            return 1.0

        remaining_fade = self.duration_secs - elapsed_secs
        return max(0.0, min(1.0, remaining_fade / self.fade_secs))

    def get_ui_metrics(self, elapsed_secs: float) -> UIMetrics:
        """Calculates rendering metrics for UI components.

        Args:
            elapsed_secs: Time elapsed since the timer started.

        Returns:
            A dictionary matching UIMetrics containing formatted time, progress ratio,
            and current phase status ('PLAYING', 'FADING', or 'BLACKOUT').
        """
        remaining = max(0.0, self.duration_secs - elapsed_secs)
        progress_ratio = remaining / self.duration_secs if self.duration_secs > 0 else 0.0

        mins, secs = divmod(int(remaining), 60)
        time_str = f"{mins:02d}:{secs:02d}"

        fade_start = self.duration_secs - self.fade_secs
        if elapsed_secs >= self.duration_secs:
            phase = "BLACKOUT"
        elif elapsed_secs >= fade_start:
            phase = "FADING"
        else:
            phase = "PLAYING"

        return {
            "time_string": time_str,
            "progress": progress_ratio,
            "phase": phase,
        }