"""keypress - A module for detecting a single keypress.

adapted from from The Python Apprentice by Robert Smallshire, Austin Bingham
"""

try:
    # only exists on Windows
    import msvcrt

    def getkey():
        """Wait for a keypress and return a single character string."""
        return msvcrt.getch().decode()

except ImportError:
    # meaning this is MacOS or Linux

    import sys
    import tty
    import termios

    def getkey():
        """Wait for a keypress and return a single character string."""
        fd = sys.stdin.fileno()
        original_attributes = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, original_attributes)
        return ch

    # If either of the Unix-specific tty or termios modules are
    # not found, the ImportError will propagate from here