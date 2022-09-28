
import signal

import os
import sys


if len(sys.argv) != 2:
    exit(-1)


os.kill(int(sys.argv[1]), signal.SIGTERM)
