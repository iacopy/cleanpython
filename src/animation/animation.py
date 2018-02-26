"""
Animation example.
"""
# 3rd party
import numpy as np
from imageio import mimwrite

FRAMES = []

for i in range(100):
    FRAMES.append(np.random.randint(0, 255, (50, 50), np.uint8))

mimwrite('output.gif', FRAMES)
