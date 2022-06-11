"""Copy and paste from system buffer with xclip linux."""

import subprocess


class Clerk():
    """Help class for work with xclip."""

    @staticmethod
    def paste():
        """Paste from system buffer and return."""
        with subprocess.Popen(['xclip', '-selection', 'c', '-o'],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              close_fds=True) as popen:
            stdout, _ = popen.communicate()
            return stdout.decode('utf-8')

    @staticmethod
    def copy(text):
        """Copy to system buffer."""
        with subprocess.Popen(['xclip', '-selection', 'c'],
                              stdin=subprocess.PIPE,
                              close_fds=True) as popen:
            popen.communicate(input=text.encode('utf-8'))
