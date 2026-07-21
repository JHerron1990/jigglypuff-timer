"""Unit tests for the timer state engine."""

import pytest
from engine import TimerEngine


def test_invalid_fade_duration_raises_error() -> None:
    """Instantiating with a fade longer than total duration must raise ValueError."""
    with pytest.raises(ValueError, match="Fade duration cannot be longer than total duration"):
        TimerEngine(duration_secs=10, fade_secs=20)


def test_volume_before_fade() -> None:
    """Volume should remain at maximum before the fade window is reached."""
    engine = TimerEngine(duration_secs=100, fade_secs=20)
    assert engine.get_volume(elapsed_secs=50) == 1.0


def test_volume_during_fade() -> None:
    """Volume should smoothly decay halfway through the fade window."""
    engine = TimerEngine(duration_secs=100, fade_secs=20)
    
    # Fade starts at 80s and ends at 100s; 90s is midpoint decay.
    assert engine.get_volume(elapsed_secs=90) == pytest.approx(0.5)


def test_volume_after_expiration() -> None:
    """Volume should remain at zero once total duration is reached or exceeded."""
    engine = TimerEngine(duration_secs=100, fade_secs=20)
    assert engine.get_volume(elapsed_secs=100) == 0.0
    assert engine.get_volume(elapsed_secs=105) == 0.0


@pytest.mark.parametrize(
    "elapsed_secs, expected_time, expected_progress, expected_phase",
    [
        (50, "00:50", 0.5, "PLAYING"),   # Midpoint play state
        (90, "00:10", 0.1, "FADING"),    # Midpoint fade state
        (100, "00:00", 0.0, "BLACKOUT"), # Expired state
    ],
)
def test_ui_metrics_phases(
    elapsed_secs: float,
    expected_time: str,
    expected_progress: float,
    expected_phase: str,
) -> None:
    """UI metrics should accurately report formatted string, progress ratio, and phase."""
    engine = TimerEngine(duration_secs=100, fade_secs=20)
    metrics = engine.get_ui_metrics(elapsed_secs)

    assert metrics["time_string"] == expected_time
    assert metrics["progress"] == pytest.approx(expected_progress)
    assert metrics["phase"] == expected_phase