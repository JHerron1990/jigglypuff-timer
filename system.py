"""OS-native system execution commands for Windows platform management."""

import logging
import subprocess

logger = logging.getLogger(__name__)


def put_to_sleep() -> bool:
    """Puts the Windows operating system into a low-power Sleep state.

    Returns:
        bool: True if the execution command succeeded, False otherwise.
    """
    logger.info("Initiating Windows Sleep sequence...")
    try:
        # Note: SetSuspendState signature is (Hibernate, ForceCritical, DisableWakeEvent).
        # Passing arguments via rundll32 is an unsupported Win32 API quirk, but standard
        # for CLI scripts. If Hibernation is enabled on the OS, Windows will default to 
        # Hibernating rather than Sleeping regardless of the '0' flag.
        subprocess.run(
            ["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"], 
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as err:
        logger.error(f"Failed to execute Windows sleep command: {err}")
        return False