import numpy as np
import pyvista as pv

# Initialize empty list to store shape's coordinates
vertices = []

# Get shape's coordinates from user input
print("Enter shape's coordinates using dashes, e.g. 'x1 y1 - x2 y2 - ...'")
print("Enter 'q' when finished.")
while True:
    coordinates = input()
    if coordinates.lower() == 'q':
        break
    coordinates = coordinates.split("-")
    for coord in coordinates:
        x, y = coord.strip().split()
        vertices.append([float(x), float(y), 0])

# Create the shape's faces
n = len(vertices)
faces = []
for i in range(n-2):
    faces.append([0, i+1, i+2])

# Create the 2D shape
shape = pv.PolyData(vertices, faces)

# Elevate it to 3D
elevated_shape = shape.elevate()

# Show the 3D shape
p = pv.Plotter()
p.add_mesh(elevated_shape)
p.show()
