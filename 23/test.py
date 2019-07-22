from best_sol import BoundingBox
import numpy

box = BoundingBox(numpy.array([
        [1, 2],
        [4, 8],
        [16, 32],
        [-64, 128]
    ]))

print(box.box)
box.minimize_bounds()
print(box.box)
box.minimize_bounds()
print(box.box)
