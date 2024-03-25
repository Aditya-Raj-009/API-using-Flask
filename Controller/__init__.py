import os
import glob

# __all__ = ['user_controller']

# or if there multiple files:

__all__ = [os.path.basename(fname)[:-3] for fname in glob.glob(os.path.dirname(__file__)+"/*.py")]