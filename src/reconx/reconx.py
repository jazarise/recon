import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'reconx'))

#!/usr/bin/env python
from cli.main import app

if __name__ == "__main__":
    app()
