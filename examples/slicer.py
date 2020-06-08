import numpy as np
import math
import compas

from compas.geometry import scale_vector
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Plane
from compas.geometry import Polyline
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.geometry import Scale
from compas.datastructures import Mesh

from compas_viewers.objectviewer import ObjectViewer

from compas_cgal.slicer import slice_mesh


# ==============================================================================
# Get the bunny and construct a mesh
# ==============================================================================

# replace by benchy

bunny = Mesh.from_ply(compas.get('bunny.ply'))

# ==============================================================================
# Move the bunny to the origin and rotate it upright.
# ==============================================================================

vector = scale_vector(bunny.centroid(), -1)
T = Translation.from_vector(vector)
S = Scale.from_factors([100, 100, 100])
R = Rotation.from_axis_and_angle(Vector(1, 0, 0), math.radians(90))

bunny.transform(R * S * T)

# ==============================================================================
# Create planes
# ==============================================================================

# replace by planes along a curve

bbox = bunny.bounding_box()

x, y, z = zip(*bbox)
xmin, xmax = min(x), max(x)

normal = Vector(1, 0, 0)
planes = []
for i in np.linspace(xmin, xmax, 100):
    plane = Plane(Point(i, 0, 0), normal)
    planes.append(plane)

# ==============================================================================
# Slice
# ==============================================================================

pointsets = slice_mesh(
    bunny.to_vertices_and_faces(),
    planes)

# ==============================================================================
# Process output
# ==============================================================================

polylines = []
for points in pointsets:
    # otherwise Polygon throws an error
    points = [Point(*point) for point in points]
    polyline = Polyline(points)
    polylines.append(polyline)

# ==============================================================================
# Visualize
# ==============================================================================

viewer = ObjectViewer()
viewer.view.use_shaders = False

for polyline in polylines:
    viewer.add(polyline, settings={'color': '#0000ff'})

viewer.update()
viewer.show()
