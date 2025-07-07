import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.memory import embed_brain
embed_brain("knowledge/brain.pdf")
