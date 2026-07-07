"""Pure mathematical state engine for the timer."""


class TimerEngine:
    """Manages the state and volume calculations independently of hardware."""

    def __init__(self, duration_secs: float, fade_secs: float) -> None:
        if fade_secs > duration_secs:
            raise ValueError("Fade duration cannot be longer than total duration.")
        
        self.duration_secs = duration_secs
        self.fade_secs = fade_secs

    def get_volume(self, elapsed_secs: float) -> float:
        """Calculate the target volume based on elapsed time."""
        if elapsed_secs >= self.duration_secs:
            return 0.0
        
        fade_start = self.duration_secs - self.fade_secs
        if elapsed_secs < fade_start:
            return 1.0
            
        # Linear decay calculation
        remaining_fade = self.duration_secs - elapsed_secs
        return max(0.0, min(1.0, remaining_fade / self.fade_secs))