import os
import sys

def restart():
      python = sys.executable
      os.execv(python, [python] + sys.argv)