#!/usr/bin/env python3
"""Command-line entry point for bloodgroup_checker."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from bloodgroup_checker.cli import main

if __name__ == "__main__":
    main()