"""Unit tests for the timer state engine."""

import pytest
from engine import TimerEngine


def test_volume_before_fade() -> None:
    """Volume should remain at maximum before the fade window is reached."""
    engine = TimerEngine(duration_secs=100, fade_secs=20)
    assert engine.get_volume(elapsed_secs=50) == 1.0


def test_volume_during_fade() -> None:
    """Volume should smoothly decay halfway through the fade window."""
    engine = TimerEngine(duration_secs=100, fade_secs=20)
    # Fade starts at 80s, ends at 100s. 90s is exactly halfway.
    assert engine.get_volume(elapsed_secs=90) == pytest.approx(0.5)


def test_volume_after_expiration() -> None:
    """Volume should hit absolute zero once elapsed time meets or exceeds duration."""
    engine = TimerEngine(duration_secs=100, fade_secs=20)
    assert engine.get_volume(elapsed_secs=100) == 0.0
    assert engine.get_volume(elapsed_secs=105) == 0.0