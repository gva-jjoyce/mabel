"""
Test the mabel logger, this extends the Python logging logger.
We test that the trace method and decorators raise no errors.
"""
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from mabel.logging.google_cloud_logger import GoogleLogger


if __name__ == "__main__":  # pragma: no cover
    GoogleLogger().warning("Noooooo")
