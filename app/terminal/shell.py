import os
import pty
import fcntl


class Shell:

    def __init__(self):

        self.pid, self.fd = pty.fork()

        if self.pid == 0:
            os.execvp("bash", ["bash"])

        flags = fcntl.fcntl(
            self.fd,
            fcntl.F_GETFL
        )

        fcntl.fcntl(
            self.fd,
            fcntl.F_SETFL,
            flags | os.O_NONBLOCK
        )

    def read(self):

        return os.read(
            self.fd,
            4096
        ).decode(errors="ignore")

    def write(self, text):

        os.write(
            self.fd,
            text.encode())