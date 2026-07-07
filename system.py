"""OS-native system execution commands for Windows."""

import logging
import subprocess

logger = logging.getLogger(__name__)


def put_to_sleep() -> bool:
    """Puts the Windows operating system into a low-power Sleep state.

    Returns:
        bool: True if the command executed successfully, False otherwise.
    """
    logger.info("Initiating Windows Sleep sequence...")
    try:
        # Calls the Windows power management API to force standard sleep
        subprocess.run(
            ["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"], 
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed to execute Windows sleep command: {e}")
        return False